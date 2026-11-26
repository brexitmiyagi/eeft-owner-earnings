# Writes results/eeft_live_model.xlsx: the same model as model.py, but every calculated cell is an
# Excel formula pointing at the Inputs sheet, so changing an input re-values the stock in the sheet.
# Also writes a dated Monitor sheet: the five series that decide the call and when they come out.
import csv, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.workbook.defined_name import DefinedName

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data')
I = {r['item']: (float(r['value']), r['source']) for r in csv.DictReader(open(os.path.join(D, 'model_inputs.csv')))}
SOFR = {r['contract']: float(r['implied_rate_pct']) / 100 for r in csv.DictReader(open(os.path.join(D, 'sofr_futures_2026-11-25.csv')))}

wb = Workbook()
ws = wb.active
ws.title = 'Inputs'
BOLD = Font(bold=True)
BLUE = Font(color='0000FF')          # blue = input you can change
FILL = PatternFill('solid', fgColor='FFF2CC')
ws.append(['Input', 'Value', 'Source / note'])
for c in ws[1]:
    c.font = BOLD

def add(name, value, note):
    ws.append([name, value, note])
    r = ws.max_row
    ws.cell(r, 2).font = BLUE
    ws.cell(r, 2).fill = FILL
    wb.defined_names[name] = DefinedName(name, attr_text=f"Inputs!$B${r}")

# filed numbers
for k in ('price', 'basic_shares_m', 'ria_q4_2025_adjusted_oi_m', 'epay_q4_2025_oi_m', 'interest_exp_q3_2026_m', 'interest_inc_q3_2026_m',
          'convert_2030_m', 'convert_coupon', 'sofr_2026_11_24', 'revolver_margin', 'tax_rate_operating', 'tax_rate_interest',
          'capex_guide_2026_mid_m', 'capex_9m_2026_m', 'dep_ttm_m', 'amort_q3_2026_m', 'non_usd_revenue_share'):
    add(k, I[k][0], I[k][1])
# my assumptions
add('cost_of_equity', 0.10, 'My valuation rate (Damodaran Nov inputs give 9.35%)')
add('g_pi_legacy', -0.007, 'Legacy Payments Infrastructure, constant currency, a year (legacy_pi.py)')
add('g_epay_2027', -0.02, 'Steam physical gift cards gone for a full year')
add('g_epay_later', 0.0, 'epay from 2028')
add('ria_q4_yoy', -0.35, 'Ria Q4 2026 vs $57.6m adjusted Q4 2025')
add('ria_q4_print', '=ria_q4_2025_adjusted_oi_m*(1+ria_q4_yoy)', 'PLAYBOOK: type the actual Q4 print here (in $m) to re-base 2027; default is my forecast')
add('ria_q1_2027_base', '=0.357*(43.3+37.3)', 'Q1 was 35.3% (2024) and 36.1% (2025) of that year Q2+Q3')
add('g_ria_after', 0.0, 'Ria growth a year after the shocked level')
add('corecard_pre_ppa_q', 8.3, 'CoreCard Q3 2026 run rate before purchase amortization')
add('corecard_loss_2028', 27.1, 'All of CoreCard 2026 profit goes with Apple from 2028 (harsh)')
add('corp_q', -26.0, 'Corporate costs a quarter')
add('fx_change', 0.0, '+0.10 = dollar 10% weaker against Euronet currencies')
add('floating_debt_m', 689.1 + 445.7, 'Revolver $689.1m + uncommitted lines $445.7m')
add('refi_spread', 0.01075 + 0.00175, 'Revolver margin + facility fee, used for the 2030 refinancing')
add('ppa_corecard_q', 4.75, 'Apple relationship amortization a quarter, to Q1 2028')
add('ppa_after_q', 0.56, 'Remaining CoreCard amortization a quarter')
# SOFR futures by calendar year (four contracts each)
for y in ('27', '28', '29', '30'):
    add(f'sofr_20{y}', round(sum(SOFR[m + y] for m in ('MAR', 'JUN', 'SEP', 'DEC')) / 4, 6), f'CME 3m SOFR futures settles 25 Nov 2026, average of 20{y} contracts')
add('consensus_eps_2026', I['consensus_adj_eps_2026'][0], 'Seeking Alpha consensus mean, 26 Nov 2026')
add('consensus_eps_2027', I['consensus_adj_eps_2027'][0], 'Seeking Alpha consensus mean, 26 Nov 2026')
add('adj_eps_9m_2026', I['adj_eps_q1_2026'][0] + I['adj_eps_q2_2026'][0] + I['adj_eps_q3_2026'][0], 'Q1-Q3 2026 releases')
add('adj_earnings_9m_2026', 62.6 + 110.0 + 137.0, 'Q1-Q3 2026 releases, $m')
add('adj_shares_q3_m', I['adj_diluted_shares_q3_m'][0], 'Q3 2026 release')
add('buyback_q_m', I['buyback_per_quarter_m'][0], 'Repurchases a quarter, Q2-Q3 2026 10-Qs')
add('net_interest_2026_m', (14.1 - 4.1) + (20.6 - 4.8) + (21.7 - 5.0) + (21.7 - 5.0), 'Q1-Q3 actual + Q4 at the Q3 run rate')
add('adj_tax_rate', 102.2 / 412.0, 'Q1-Q3 2026 adjusted tax / adjusted pre-tax')
add('cash_sep26_m', 955.4, 'Q3 2026 10-Q (XBRL CashAndCashEquivalentsAtCarryingValue)')
add('total_assets_sep26_m', 6054.1, 'Q3 2026 10-Q (XBRL Assets)')
add('debt_sep26_m', 470.5 + 1706.2, 'Q3 2026 10-Q: current 470.5 + noncurrent 1706.2 (XBRL)')
add('total_liabilities_sep26_m', 4753.8, 'Q3 2026 10-Q (XBRL Liabilities)')
add('equity_sep26_m', 1300.3, 'Q3 2026 10-Q, including non-controlling interest (XBRL)')
add('hold_line', '=price*1.0435', 'Value needed for HOLD: expected return of at least 4.35% (my 9.35% cost of equity less 5 points)')
ws.column_dimensions['A'].width = 30
ws.column_dimensions['B'].width = 14
ws.column_dimensions['C'].width = 95

# ---- Quarterly ----
q = wb.create_sheet('Quarterly')
hdr = ['Period', 'Year', 'Legacy PI', 'CoreCard pre-PPA', 'PPA', 'PI', 'epay', 'Ria', 'Corporate', 'Operating income', 'fx multiplier']
q.append(hdr)
for c in q[1]:
    c.font = BOLD
periods = [('Q4', 2026)] + [(qq, y) for y in (2027, 2028) for qq in ('Q1', 'Q2', 'Q3', 'Q4')]
pi_base = {'Q4': 44.07, 'Q1': 23.05, 'Q2': 83.95, 'Q3': 124.65}
ria_26 = {'Q2': 43.3, 'Q3': 37.3}
epay_26 = {'Q1': 32.4, 'Q2': 32.8, 'Q3': 31.8}
row_of = {}
for i, (qq, y) in enumerate(periods):
    r = i + 2
    row_of[(qq, y)] = r
    # legacy PI: same quarter a year earlier, grown
    prev = row_of.get((qq, y - 1))
    leg = f'=C{prev}*(1+g_pi_legacy)' if prev else f'={pi_base[qq]}*(1+g_pi_legacy)'
    cc = '=corecard_pre_ppa_q-corecard_loss_2028/4' if y == 2028 else '=corecard_pre_ppa_q'
    ppa = '=ppa_corecard_q' if (y < 2028 or qq == 'Q1') else '=ppa_after_q'
    if (qq, y) == ('Q4', 2026):
        ria = '=ria_q4_print'
        epay = '=epay_q4_2025_oi_m*(1-0.03)'
    elif y == 2027:
        scale = f'(ria_q4_print/(ria_q4_2025_adjusted_oi_m*(1+ria_q4_yoy)))'
        if qq == 'Q1':
            ria = f'=ria_q1_2027_base*{scale}*(1+g_ria_after)'
        elif qq in ('Q2', 'Q3'):
            ria = f'={ria_26[qq]}*{scale}*(1+g_ria_after)'
        else:
            ria = f'=H{row_of[("Q4", 2026)]}*(1+g_ria_after)'
        epay = f'=G{row_of[("Q4", 2026)]}*(1+g_epay_2027)' if qq == 'Q4' else f'={epay_26[qq]}*(1+g_epay_2027)'
    else:
        ria = f'=H{prev}*(1+g_ria_after)'
        epay = f'=G{prev}*(1+g_epay_later)'
    q.append([f'{qq} {y}', y, leg, cc, ppa, f'=C{r}+D{r}-E{r}', epay, ria, '=corp_q',
              f'=(F{r}+G{r}+H{r})*K{r}+I{r}', '=1+fx_change*non_usd_revenue_share'])
for col in 'ABCDEFGHIJK':
    q.column_dimensions[col].width = 15
for row in q.iter_rows(min_row=2, min_col=3, max_col=11):
    for c in row:
        c.number_format = '0.00'

# ---- Annual and valuation ----
a = wb.create_sheet('Valuation')
a.append(['Line', '2027', '2028', '2029', '2030', '2031 (terminal year)'])
for c in a[1]:
    c.font = BOLD
r27 = [row_of[(qq, 2027)] for qq in ('Q1', 'Q2', 'Q3', 'Q4')]
r28 = [row_of[(qq, 2028)] for qq in ('Q1', 'Q2', 'Q3', 'Q4')]
rng = lambda col, rows: f'Quarterly!{col}{rows[0]}:{col}{rows[-1]}'
# segment rows (after fx), 2029+ grow from 2028; 2028 PI adds back the Q1 Apple amortization difference
a.append(['PI (after fx)', f'=SUMPRODUCT({rng("F", r27)},{rng("K", r27)})', f'=SUMPRODUCT({rng("F", r28)},{rng("K", r28)})+(ppa_corecard_q-ppa_after_q)*Quarterly!K2',
          '=D2*0+C2*(1+g_pi_legacy)', '=D2*(1+g_pi_legacy)', '=E2*(1+g_pi_legacy)'])
a.append(['epay (after fx)', f'=SUMPRODUCT({rng("G", r27)},{rng("K", r27)})', f'=SUMPRODUCT({rng("G", r28)},{rng("K", r28)})',
          '=C3*(1+g_epay_later)', '=D3*(1+g_epay_later)', '=E3*(1+g_epay_later)'])
a.append(['Ria (after fx)', f'=SUMPRODUCT({rng("H", r27)},{rng("K", r27)})', f'=SUMPRODUCT({rng("H", r28)},{rng("K", r28)})',
          '=C4*(1+g_ria_after)', '=D4*(1+g_ria_after)', '=E4*(1+g_ria_after)'])
# operating income: 2027/28 from the quarters (2028 without the add-back), 2029+ from segments
a.append(['Operating income', f'=SUM({rng("J", r27)})', f'=SUM({rng("J", r28)})', '=SUM(D2:D4)+4*corp_q', '=SUM(E2:E4)+4*corp_q', '=SUM(F2:F4)+4*corp_q'])
a.append(['Amortization', f'=amort_q3_2026_m*4-4*ppa_corecard_q+SUM({rng("E", r27)})', f'=amort_q3_2026_m*4-4*ppa_corecard_q+SUM({rng("E", r28)})',
          '=amort_q3_2026_m*4-19+2.24', '=amort_q3_2026_m*4-19+2.24', '=E6'])
a.append(['SOFR (futures, year average)', '=sofr_2027', '=sofr_2028', '=sofr_2029', '=sofr_2030', '=sofr_2030'])
a.append(['Net interest', '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(B7-sofr_2026_11_24)',
          '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(C7-sofr_2026_11_24)',
          '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(D7-sofr_2026_11_24)',
          '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(E7-sofr_2026_11_24)+B13/4',
          '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(F7-sofr_2026_11_24)+B13'])
a.append(['Owner earnings', '=B5*(1-tax_rate_operating)-B8*(1-tax_rate_interest)+B6', '=C5*(1-tax_rate_operating)-C8*(1-tax_rate_interest)+C6',
          '=D5*(1-tax_rate_operating)-D8*(1-tax_rate_interest)+D6', '=E5*(1-tax_rate_operating)-E8*(1-tax_rate_interest)+E6',
          '=F5*(1-tax_rate_operating)-F8*(1-tax_rate_interest)+F6'])
a.append(['Discount factor', '=1/(1+cost_of_equity)^1', '=1/(1+cost_of_equity)^2', '=1/(1+cost_of_equity)^3', '=1/(1+cost_of_equity)^4', ''])
a.append([])
a.append(['Refinancing rate (revolver all-in at 2030 forward)', '=sofr_2030+refi_spread'])
a.append(['Extra interest a year once refinanced', '=convert_2030_m*(B12-convert_coupon)'])
a.append(['Terminal growth (segment-weighted)', '=(E2*g_pi_legacy+E3*g_epay_later+E4*g_ria_after)/SUM(E2:E4)'])
a.append(['Terminal value', '=F9/(cost_of_equity-B14)'])
a.append(['Q4 2026 owner earnings', f'=Quarterly!J2*(1-tax_rate_operating)-(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*(1-tax_rate_interest)+amort_q3_2026_m-((capex_guide_2026_mid_m-capex_9m_2026_m)-dep_ttm_m/4)'])
a.append(['Equity value $m', '=B16/(1+cost_of_equity)^0.25+SUMPRODUCT(B9:E9,B10:E10)+B15*E10'])
a.append(['Value per share', '=B17/basic_shares_m'])
a.append(['Price', '=price'])
a.append(['Expected return to value', '=B18/B19-1'])
a.append(['HOLD needs', '=hold_line'])
a.append(['Rating', '=IF(B20>0.1435,"BUY",IF(B20<0.0435,"SELL","HOLD"))'])
for c in ('A18', 'B18', 'A22', 'B22'):
    a[c].font = BOLD
a.column_dimensions['A'].width = 48
for col in 'BCDEF':
    a.column_dimensions[col].width = 16
for row in a.iter_rows(min_row=2, max_row=21, min_col=2, max_col=6):
    for c in row:
        c.number_format = '0.00'
for c in ('B7', 'C7', 'D7', 'E7', 'F7', 'B12', 'B14', 'B20'):
    a[c].number_format = '0.00%'
# the 2029 PI cell: tidy formula
a['D2'] = '=C2*(1+g_pi_legacy)'

# ---- Street bridge: the consensus, not mine ----
sb = wb.create_sheet('Street bridge')
for r in [['Line', 'Value', 'How'],
          ['Street Q4 2026 EPS', '=consensus_eps_2026-adj_eps_9m_2026', '2026 consensus less Q1-Q3 actual'],
          ['Q4 2026 shares (m)', '=adj_shares_q3_m-0.45', 'as model.py'],
          ['Street 2026 adjusted earnings ($m)', '=adj_earnings_9m_2026+B2*B3', ''],
          ['Implied 2026 average shares (m)', '=B4/consensus_eps_2026', ''],
          ['Shares retired a quarter (m)', '=buyback_q_m/price', 'at today\'s price'],
          ['2027 average shares (m)', '=AVERAGE(B3-B6,B3-2*B6,B3-3*B6,B3-4*B6)', 'buybacks every quarter'],
          ['1) EPS from buybacks alone', '=consensus_eps_2026*B5/B7', ''],
          ['2027 net interest on the futures curve ($m)', '=(interest_exp_q3_2026_m-interest_inc_q3_2026_m)*4+floating_debt_m*(sofr_2027-sofr_2026_11_24)', ''],
          ['2) EPS after higher interest', '=B8-(B9-net_interest_2026_m)*(1-tax_rate_interest)/B7', ''],
          ['3) Left for operations, per share', '=consensus_eps_2027-B10', ''],
          ['   as adjusted earnings ($m)', '=B11*B7', ''],
          ['   as operating income growth ($m)', '=B12/(1-adj_tax_rate)', 'what the Street needs operations to add in 2027']]:
    sb.append(r)
for c in sb[1]:
    c.font = BOLD
sb.column_dimensions['A'].width = 44; sb.column_dimensions['B'].width = 14; sb.column_dimensions['C'].width = 40
for row in sb.iter_rows(min_row=2, min_col=2, max_col=2):
    for c in row: c.number_format = '0.00'

# ---- Three statements (annual, simplified): income, cash flow, balance sheet ----
t = wb.create_sheet('3-Statement')
cols = ['Q4 2026', '2027', '2028', '2029', '2030']
t.append(['$m'] + cols)
for c in t[1]:
    c.font = BOLD
V = {'2027': 'B', '2028': 'C', '2029': 'D', '2030': 'E'}
def row(label, vals):
    t.append([label] + vals); return t.max_row
sofr = {'2027': 'sofr_2027', '2028': 'sofr_2028', '2029': 'sofr_2029', '2030': 'sofr_2030'}
r_hdr1 = row('INCOME STATEMENT', [''] * 5)
r_oi = row('Operating income', ['=Quarterly!J2'] + [f'=Valuation!{V[y]}5' for y in cols[1:]])
r_int = row('Net interest (model)', ['=interest_exp_q3_2026_m-interest_inc_q3_2026_m'] + [f'=Valuation!{V[y]}8' for y in cols[1:]])
# interest on debt paid down (negative) or added by buybacks beyond cash flow, at revolver all-in, on the opening balance change
r_dint = row('Interest on debt change since Sep 2026', ['=0'] + [None] * 4)
r_pt = row('Pre-tax income', [None] * 5)
r_tax = row('Tax', [None] * 5)
r_ni = row('Net income', [None] * 5)
r_sh = row('Average diluted shares (m)', ['=adj_shares_q3_m-0.45'] + [None] * 4)
r_eps = row('EPS (GAAP basis of the model)', [None] * 5)
r_hdr2 = row('CASH FLOW', [''] * 5)
r_ni2 = row('Net income', [None] * 5)
r_amort = row('Amortization of intangibles', ['=amort_q3_2026_m'] + [f'=Valuation!{V[y]}6' for y in cols[1:]])
r_dep = row('Depreciation', ['=dep_ttm_m/4'] + ['=dep_ttm_m'] * 4)
r_capex = row('Capex (set to depreciation; Q4 at guide)', ['=-(capex_guide_2026_mid_m-capex_9m_2026_m)'] + ['=-dep_ttm_m'] * 4)
r_fcf = row('Free cash flow', [None] * 5)
r_bb = row('Buybacks', ['=-buyback_q_m'] + ['=-4*buyback_q_m'] * 4)
r_ddebt = row('Debt drawn (repaid), cash held flat', [None] * 5)
r_hdr3 = row('BALANCE SHEET (end of period)', [''] * 5)
r_cash = row('Cash', ['=cash_sep26_m'] * 5)
r_oa = row('Other assets', [None] * 5)
r_ta = row('Total assets', [None] * 5)
r_debt = row('Debt', [None] * 5)
r_ol = row('Other liabilities', ['=total_liabilities_sep26_m-debt_sep26_m'] * 5)
r_eq = row('Equity', [None] * 5)
r_chk = row('Check: assets - liabilities - equity', [None] * 5)
letters = 'BCDEF'
for i, col in enumerate(letters):
    prev = letters[i - 1] if i else None
    y = cols[i]
    if i:
        t[f'{col}{r_dint}'] = f'=({prev}{r_debt}-debt_sep26_m)*({sofr[y]}+refi_spread)'
        t[f'{col}{r_sh}'] = (f'={prev}{r_sh}-2.5*buyback_q_m/price' if i == 1 else f'={prev}{r_sh}-4*buyback_q_m/price')   # yearly averages at today's price
    t[f'{col}{r_pt}'] = f'={col}{r_oi}-{col}{r_int}-{col}{r_dint}'
    t[f'{col}{r_tax}'] = f'=-({col}{r_oi}*tax_rate_operating-({col}{r_int}+{col}{r_dint})*tax_rate_interest)'
    t[f'{col}{r_ni}'] = f'={col}{r_pt}+{col}{r_tax}'
    t[f'{col}{r_eps}'] = f'={col}{r_ni}/{col}{r_sh}'
    t[f'{col}{r_ni2}'] = f'={col}{r_ni}'
    t[f'{col}{r_fcf}'] = f'={col}{r_ni2}+{col}{r_amort}+{col}{r_dep}+{col}{r_capex}'
    t[f'{col}{r_ddebt}'] = f'=-({col}{r_fcf}+{col}{r_bb})'
    oa_prev = f'(total_assets_sep26_m-cash_sep26_m)' if not i else f'{prev}{r_oa}'
    t[f'{col}{r_oa}'] = f'={oa_prev}-{col}{r_amort}-{col}{r_dep}-{col}{r_capex}'
    t[f'{col}{r_ta}'] = f'={col}{r_cash}+{col}{r_oa}'
    debt_prev = 'debt_sep26_m' if not i else f'{prev}{r_debt}'
    t[f'{col}{r_debt}'] = f'={debt_prev}+{col}{r_ddebt}'
    eq_prev = 'equity_sep26_m' if not i else f'{prev}{r_eq}'
    t[f'{col}{r_eq}'] = f'={eq_prev}+{col}{r_ni}+{col}{r_bb}'
    t[f'{col}{r_chk}'] = f'=ROUND({col}{r_ta}-{col}{r_debt}-{col}{r_ol}-{col}{r_eq},6)'
for rr in (r_hdr1, r_hdr2, r_hdr3):
    t.cell(rr, 1).font = BOLD
t.column_dimensions['A'].width = 42
for col in letters:
    t.column_dimensions[col].width = 12
for rw in t.iter_rows(min_row=2, min_col=2, max_col=6):
    for c in rw: c.number_format = '0.0'
t.append([])
t.append(['Simplified: other assets and other liabilities (settlement balances, ATM cash, goodwill, leases) held at their 30 Sep 2026 levels; debt is the balancing item with cash held flat; the convertible refinancing sits in net interest. The valuation sheet values owner earnings; this sheet shows where the cash goes and checks that it balances.'])

# ---- Monitor ----
mo = wb.create_sheet('Monitor')
mo.append(['EEFT: five series that decide the call', '', '', '', 'As of 26 Nov 2026'])
mo['A1'].font = Font(bold=True, size=13)
mo.append([])
mo.append(['Series', 'Where', 'Next release', 'Last reading', 'What moves the call'])
for c in mo[3]:
    c.font = BOLD
rows = [
    ['Euronet Q4 2026 release: Ria operating income, legacy PI in constant currency, adjusted EPS',
     'Euronet 8-K (SEC EDGAR)', 'Not announced; Q4 2025 came 12 Feb 2026 and Q4 2024 on 13 Feb 2025',
     'Q3 2026: Ria $37.3m (-37%), EPS $3.55',
     'Ria above $46.6m = HOLD; $39.6-46.6m HOLD only with growth evidence; below $33m value toward $60. Forecast: Ria $37.4m ($33-42m), EPS $2.26 ($2.15-2.45)'],
    ['Banxico remittances: number of transfers and average size',
     'Banxico monthly release', 'Early each month for the month before (Aug data 1 Oct, Sep data 3 Nov); October data expected early December',
     'Jan-Sep: 114.9m transfers (-2.7%), average $411 (+5%)',
     'Counts falling and average flat or down = precautionary sending exhausted, totals likely turn. Counts flattening = supports the 2% Ria growth case'],
    ['Honduras remittances (BCH)', 'BCH figures as reported by La Tribuna / El Heraldo', 'BCH publishes running year-to-date totals; I check monthly',
     'Jan-Sep +11.2%; BCH survey average send $510.30 vs $451.80',
     'Inflow growth turning negative = senders leaving, not switching channel'],
    ['EMBI spreads: Honduras, El Salvador, Guatemala', 'J.P. Morgan EMBI via Bloomberg Linea month-end table',
     'First days of each month (October table 3 Nov 2026)', 'End-Oct 204 / 317 / 142bp (end-July 164 / 275 / 122)',
     'Further widening alongside falling counts confirms the warning reading'],
    ['CME 3-month SOFR futures, 2027-2030 strip', 'CME Group settlements', 'Daily',
     '25 Nov 2026: 2027 4.54%, 2028 4.30%, 2029 4.24%, 2030 4.29%',
     'Each 1 point on SOFR changes interest by about $11.3m a year on $1,135m of floating debt'],
]
for r in rows:
    mo.append(r)
mo.append([])
mo.append(['Also on my side: the weekly $400 price index (Ria vs Western Union, Remitly, Xoom, Wise) and the Ria US agent sample, both rerun from scripts.'])
for col, wdt in zip('ABCDE', (44, 34, 40, 40, 60)):
    mo.column_dimensions[col].width = wdt
for row in mo.iter_rows(min_row=3, max_row=8):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')
mo.page_setup.orientation = 'landscape'
mo.page_setup.fitToWidth = 1
mo.page_setup.fitToHeight = 1
mo.sheet_properties.pageSetUpPr.fitToPage = True

out = os.path.join(HERE, '..', 'results', 'eeft_live_model.xlsx')
wb.save(out)
print('saved', out)

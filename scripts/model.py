# The EEFT model: quarterly segments Q4 2026 to Q4 2028, years to 2030, a terminal value after the
# convertible is refinanced, owner earnings, net debt, share count, my adjusted EPS vs consensus,
# a Q4 2026 forecast, and the currency line. Every assumption is a named variable at the top.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
I = {r['item']: float(r['value']) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'model_inputs.csv')))}
OUT = os.path.join(HERE, '..', 'results')

# ---- assumptions (central case) ----
K = 0.10                     # cost of equity I value at
G_PI_LEGACY = -0.007         # legacy Payments Infrastructure, constant currency (legacy_pi.py)
G_EPAY_2027 = -0.02          # Steam's physical gift cards gone for a full year
G_EPAY_LATER = 0.0
RIA_Q4_YOY = -0.35           # Q4 2026 vs the $57.6m adjusted Q4 2025, in line with Q2 (-34%) and Q3 (-37%)
RIA_Q1_2027 = 0.357 * (43.3 + 37.3)   # Q1 was 35.3% (2024) and 36.1% (2025) of that year's Q2+Q3; applied to 2026's Q2+Q3
G_RIA_AFTER = 0.0            # flat from the shocked level
CORECARD_PRE_PPA_Q = 8.3     # Q3 2026 run rate before purchase amortization
CORECARD_LOSS_2028 = 27.1    # all of CoreCard's 2026 operating income goes with Apple from Q1 2028 (harsh)
CORP_Q = -26.0
REFI_RATE = None   # set after the curve loads: revolver all-in at the 2030 forward SOFR
G_TERMINAL = None            # set below as the segment-weighted rate
TAX_OP, TAX_INT = I['tax_rate_operating'], I['tax_rate_interest']
# CME 3-month SOFR futures, settles 25 Nov 2026 (data/sofr_futures_2026-11-25.csv): average implied rate by calendar year,
# each year = the four contracts starting in it. Floating debt = revolver $689.1m + uncommitted lines $445.7m (I assume both float).
import csv as _csv
_c = {r['contract']: float(r['implied_rate_pct']) / 100 for r in _csv.DictReader(open(os.path.join(HERE, '..', 'data', 'sofr_futures_2026-11-25.csv')))}
SOFR_YEAR = {y: sum(_c[m + y[2:]] for m in ('MAR', 'JUN', 'SEP', 'DEC')) / 4 for y in ('2027', '2028', '2029', '2030')}
FLOATING_DEBT = 689.1 + 445.7
USE_CURVE = True
REFI_RATE = SOFR_YEAR['2030'] + I['revolver_margin'] + 0.00175   # revolver all-in (margin 1.075% + 0.175% fee) at the futures-implied 2030 SOFR; BBB index 6.09% is the high case

def run(k=K, g_pi=G_PI_LEGACY, ria_q4=RIA_Q4_YOY, g_ria=G_RIA_AFTER, g_epay27=G_EPAY_2027, refi=None,
        corecard_loss=CORECARD_LOSS_2028, fx=0.0, ria_q1_27=None, tax_op=None, tax_int=None, use_curve=USE_CURVE, floating=None, ria_scale=1.0, ria_add_q=0.0, verbose=False):
    fl = FLOATING_DEBT if floating is None else floating
    refi = REFI_RATE if refi is None else refi
    TAX_OP_ = I['tax_rate_operating'] if tax_op is None else tax_op
    TAX_INT_ = I['tax_rate_interest'] if tax_int is None else tax_int
    q1_27 = RIA_Q1_2027 if ria_q1_27 is None else ria_q1_27
    # fx: change in non-dollar profits from currency (e.g. -0.10 for a 10% stronger dollar)
    fxm = 1 + fx * I['non_usd_revenue_share'] / 1.0
    # legacy PI quarters (TTM base from legacy_pi.py: Q4'25 44.07, Q1 23.05, Q2 83.95, Q3 124.65)
    pi_leg = {'Q4': 44.07, 'Q1': 23.05, 'Q2': 83.95, 'Q3': 124.65}
    ria_26 = {'Q1': 41.9, 'Q2': 43.3, 'Q3': 37.3}
    epay_26 = {'Q1': 32.4, 'Q2': 32.8, 'Q3': 31.8, 'Q4': I['epay_q4_2025_oi_m']}
    qs = [('2026', 'Q4')] + [(str(y), q) for y in (2027, 2028) for q in ('Q1', 'Q2', 'Q3', 'Q4')]
    rows = []
    leg, ria, epay = dict(pi_leg), {}, dict(epay_26)
    for y, q in qs:
        leg[q] = leg[q] * (1 + g_pi)
        if (y, q) == ('2026', 'Q4'):
            ria_q = I['ria_q4_2025_adjusted_oi_m'] * (1 + ria_q4)
            epay_q = epay_26['Q4'] * (1 - 0.03)            # Q3 was +3% reported; Steam takes it negative
        elif y == '2027':
            base = {'Q1': q1_27 * ria_scale, 'Q2': ria_26['Q2'] * ria_scale, 'Q3': ria_26['Q3'] * ria_scale,
                    'Q4': I['ria_q4_2025_adjusted_oi_m'] * (1 + ria_q4)}[q]   # ria_scale: re-base 2027 if the Q4 print surprises
            ria_q = base * (1 + g_ria) + ria_add_q   # ria_add_q: e.g. Ria's 2026 SG&A step-up reversed
            epay_q = epay[q] * (1 + g_epay27) if q != 'Q4' else epay[q] * (1 - 0.03) * (1 + g_epay27) / (1 - 0.03)
        else:
            ria_q = ria[q] * (1 + g_ria)
            epay_q = epay[q] * (1 + G_EPAY_LATER)
        ria[q], epay[q] = ria_q, epay_q
        cc_pre = CORECARD_PRE_PPA_Q - (corecard_loss / 4 if y == '2028' else 0)
        ppa = 4.75 if (y, q) < ('2028', 'Q2') else 0.56
        pi_q = leg[q] + cc_pre - ppa
        oi = (pi_q + epay_q + ria_q) * fxm + CORP_Q
        rows.append(dict(period=f"{q} {y}", pi=pi_q * fxm, pi_legacy=leg[q] * fxm, corecard=cc_pre - ppa, epay=epay_q * fxm, ria=ria_q * fxm,
                         corp=CORP_Q, oi=oi, ppa=ppa))
    # annual roll-up 2027-2030, then terminal
    net_int_q = I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m']
    refi_extra = I['convert_2030_m'] * (refi - I['convert_coupon'])     # a year, pre-tax, once refinanced
    amort_q = I['amort_q3_2026_m']
    years = {}
    for y in ('2027', '2028'):
        oi = sum(r['oi'] for r in rows if r['period'].endswith(y))
        ppa = sum(r['ppa'] for r in rows if r['period'].endswith(y))
        years[y] = dict(oi=oi, amort=amort_q * 4 - 4 * 4.75 + ppa)
    seg28 = {s: sum(r[s] for r in rows if r['period'].endswith('2028')) for s in ('pi', 'epay', 'ria')}
    seg28['pi'] += (4.75 - 0.56) * fxm     # Q1 2028 still carried the Apple relationship's amortization; it's gone from 2029
    for y in ('2029', '2030'):
        prev = seg28 if y == '2029' else years['2029']['seg']
        seg = {'pi': prev['pi'] * (1 + g_pi), 'epay': prev['epay'] * (1 + G_EPAY_LATER), 'ria': prev['ria'] * (1 + g_ria)}
        years[y] = dict(oi=sum(seg.values()) + 4 * CORP_Q, amort=amort_q * 4 - 19.0 + 2.24, seg=seg)
    oe = {}
    for y, d in years.items():
        curve = fl * (SOFR_YEAR[y] - I['sofr_2026_11_24']) if use_curve else 0.0
        interest = net_int_q * 4 + curve + (refi_extra / 4 if y == '2030' else 0)
        # owner earnings = net income + D&A - maintenance capex; with maintenance capex = depreciation
        # (growth capex, the ~$2.7m a year above depreciation, is left out), that's net income + amortization
        oe[y] = d['oi'] * (1 - TAX_OP_) - interest * (1 - TAX_INT_) + d['amort']
    # terminal: 2031 with the full refinancing, growing at the segment-weighted rate
    s30 = years['2030']['seg']
    w = sum(s30.values())
    g_t = (s30['pi'] * g_pi + s30['epay'] * G_EPAY_LATER + s30['ria'] * g_ria) / w
    oi31 = sum(v * (1 + {'pi': g_pi, 'epay': G_EPAY_LATER, 'ria': g_ria}[s]) for s, v in s30.items()) + 4 * CORP_Q
    curve31 = fl * (SOFR_YEAR['2030'] - I['sofr_2026_11_24']) if use_curve else 0.0
    oe31 = oi31 * (1 - TAX_OP_) - (net_int_q * 4 + curve31 + refi_extra) * (1 - TAX_INT_) + years['2030']['amort']
    tv = oe31 / (k - g_t)
    # Q4 2026 owner earnings, received in about a quarter
    q4 = rows[0]
    q4_capex = I['capex_guide_2026_mid_m'] - I['capex_9m_2026_m']          # what the $140m guide midpoint leaves for Q4
    oe_q4 = q4['oi'] * (1 - TAX_OP_) - net_int_q * (1 - TAX_INT_) + amort_q - (q4_capex - I['dep_ttm_m'] / 4)
    pv = oe_q4 / (1 + k) ** 0.25
    for i, y in enumerate(('2027', '2028', '2029', '2030'), start=1):
        pv += oe[y] / (1 + k) ** (i + 0.0)
    pv += tv / (1 + k) ** 4
    per_share = pv / I['basic_shares_m']
    if verbose:
        return per_share, rows, years, oe, oe31, g_t, tv, pv, oe_q4, refi_extra
    return per_share

if __name__ == '__main__':
    v, rows, years, oe, oe31, g_t, tv, pv, oe_q4, refi_extra = run(verbose=True)
    P = I['price']
    print("Quarterly segment operating income, $m (GAAP; PI includes CoreCard after its purchase amortization)")
    print(f"{'period':8s} {'PI':>7s} {'legacy':>7s} {'CoreCard':>8s} {'epay':>7s} {'Ria':>7s} {'corp':>7s} {'total':>7s}")
    with open(os.path.join(OUT, 'model_quarterly.csv'), 'w', newline='') as f:
        wr = csv.writer(f); wr.writerow(['period', 'pi', 'pi_legacy', 'corecard', 'epay', 'ria', 'corp', 'oi'])
        for r in rows:
            print(f"{r['period']:8s} {r['pi']:7.1f} {r['pi_legacy']:7.1f} {r['corecard']:8.1f} {r['epay']:7.1f} {r['ria']:7.1f} {r['corp']:7.1f} {r['oi']:7.1f}")
            wr.writerow([r['period']] + [round(r[k], 2) for k in ('pi', 'pi_legacy', 'corecard', 'epay', 'ria', 'corp', 'oi')])
    print(f"\nconvertible refinanced Oct 2030 at {REFI_RATE*100:.2f}% (revolver all-in at the 2030 forward SOFR) vs 0.625%: +${refi_extra:.1f}m a year pre-tax, ${refi_extra*(1-TAX_INT):.1f}m after tax")
    print(f"interest run rate today: ${(I['interest_exp_q3_2026_m']-I['interest_inc_q3_2026_m'])*4:.1f}m net a year (Q3 x4) vs ${70.8-19.4:.1f}m in the TTM")
    print(f"owner earnings: Q4 2026 ${oe_q4:.1f}m; " + ', '.join(f"{y} ${x:.1f}m" for y, x in oe.items()) + f"; 2031 ${oe31:.1f}m")
    print(f"terminal growth {g_t*100:.2f}%, terminal value ${tv:.0f}m, equity value ${pv:.0f}m")
    print(f"VALUE ${v:.2f} a share, {v/P*100-100:+.1f}% vs ${P}")
    print(f"BUY below ${v/1.1435:.2f}, SELL above ${v/1.0435:.2f}")
    print(f"  no refinancing at all (0.625% forever): ${run(refi=I['convert_coupon']):.2f}")
    print(f"  SOFR held at today's 3.94% instead of the futures curve: ${run(use_curve=False, refi=I['sofr_2026_11_24'] + I['revolver_margin'] + 0.00175):.2f}")
    print('  SOFR by year (futures): ' + ', '.join(f"{y} {r*100:.2f}%" for y, r in SOFR_YEAR.items()))
    # walk from the v5 single-stage value to this one
    steps = []
    print("\nsensitivity (one at a time):")
    for name, kw in [('cost of equity 9.35%', dict(k=0.0935)), ('cost of equity 11%', dict(k=0.11)),
                     ('refi at BBB index 6.09%', dict(refi=I['bbb_yield_2026_11_24'])), ('refi at 4.5%', dict(refi=0.045)),
                     ('Ria Q1 2027 holds at $41.9m', dict(ria_q1_27=41.9)), ('operating tax 31%', dict(tax_op=0.31)),
                     ('no tax shield on interest', dict(tax_int=0.0)), ('interest shield at 21% federal only', dict(tax_int=0.21)),
                     ('uncommitted lines not on the SOFR curve', dict(floating=689.1)),
                     ('Ria -3% a year after 2027', dict(g_ria=-0.03)), ('Ria +2% a year after 2027', dict(g_ria=0.02)),
                     ('Ria Q4 only -25%', dict(ria_q4=-0.25)), ('legacy PI -2%', dict(g_pi=-0.02)), ('legacy PI +1%', dict(g_pi=0.01)),
                     ('epay 2027 -5%', dict(g_epay27=-0.05)), ('CoreCard keeps half (loss 13.55)', dict(corecard_loss=13.55)),
                     ('dollar 10% stronger', dict(fx=-0.10)), ('dollar 10% weaker', dict(fx=0.10))]:
        x = run(**kw); print(f"  {name:34s} ${x:6.2f} ({x-v:+.2f})")
    # Q4 2026 forecast and EPS vs consensus
    q4 = rows[0]
    d_oi = (q4['pi'] - I['pi_q4_2025_oi_m']) + (q4['epay'] - I['epay_q4_2025_oi_m']) + (q4['ria'] - I['ria_q4_2025_adjusted_oi_m']) + (q4['corp'] - I['corp_q4_2025_oi_m'])
    d_int = -((I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m']) - (I['interest_exp_q4_2025_m'] - I['interest_inc_q4_2025_m']))
    # pass-through calibrated on Q3 2026: adjusted earnings fell $11.3m on a $23.4m fall in operating income
    pt = (I['adj_earnings_q3_2025_m'] - I['adj_earnings_q3_2026_m']) / 23.4
    adj_q4 = I['adj_earnings_q4_2025_m'] + pt * (d_oi + d_int)
    sh_q4 = I['adj_diluted_shares_q3_m'] - 0.45
    eps_q4_pt = adj_q4 / sh_q4
    # direct build: adjusted pre-tax = GAAP operating income + intangible amortization + share comp - net interest,
    # taxed at the 9M 2026 adjusted rate: adjusted tax 102.2 on adjusted pre-tax 412.0 (Q1-Q3 releases)
    adj_rate = 102.2 / 412.0
    adj_q4_direct = (q4['oi'] + I['amort_q3_2026_m'] + (15.7 + 16.7) / 2 - (I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m'])) * (1 - adj_rate)
    eps_q4_direct = adj_q4_direct / sh_q4
    eps_q4 = (eps_q4_pt + eps_q4_direct) / 2
    print(f"\nQ4 EPS two ways: pass-through ${eps_q4_pt:.2f}, direct build ${eps_q4_direct:.2f} (adjusted tax {adj_rate*100:.1f}%); I use the average ${eps_q4:.2f}")
    adj_q4 = eps_q4 * sh_q4
    eps26 = I['adj_eps_q1_2026'] + I['adj_eps_q2_2026'] + I['adj_eps_q3_2026'] + eps_q4
    street_q4 = I['consensus_adj_eps_2026'] - (I['adj_eps_q1_2026'] + I['adj_eps_q2_2026'] + I['adj_eps_q3_2026'])
    print(f"\nQ4 2026 FORECAST: Ria ${q4['ria']:.1f}m (vs $57.6m adjusted), legacy PI ${q4['pi_legacy']:.1f}m constant currency (vs $44.1m), "
          f"epay ${q4['epay']:.1f}m (vs $47.3m), adjusted EPS ${eps_q4:.2f} (Street implied ${street_q4:.2f}, Q4 2025 $2.39)")
    print(f"  pass-through {pt:.2f}, change in operating income {d_oi:+.1f}, change in net interest {d_int:+.1f}, adjusted earnings ${adj_q4:.1f}m on {sh_q4:.2f}m shares")
    # 2027 adjusted EPS: 2026 adjusted earnings plus after-tax changes
    oi26 = 72.0 + 137.1 + 171.6 + q4['oi']
    oi27 = years['2027']['oi']
    int26 = (14.1 - 4.1) + (20.6 - 4.8) + (21.7 - 5.0) + (I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m'])
    int27 = (I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m']) * 4 + FLOATING_DEBT * (SOFR_YEAR['2027'] - I['sofr_2026_11_24'])   # futures curve
    adj26 = 62.6 + 110.0 + 137.0 + adj_q4
    ppa_change = (sum(r['ppa'] for r in rows if r['period'].endswith('2027')) - (4.75 * 3 + 4.75))   # amortization is added back
    adj27 = adj26 + ((oi27 - oi26) + ppa_change - (int27 - int26)) * (1 - 0.25)
    sh27 = sum(sh_q4 - I['buyback_per_quarter_m'] / P * (i + 1) for i in range(4)) / 4   # average 2027: buybacks every quarter at the 2026 pace and today's price
    eps27 = adj27 / sh27
    print(f"\nMY ADJUSTED EPS vs CONSENSUS: 2026E ${eps26:.2f} vs ${I['consensus_adj_eps_2026']:.2f}; 2027E ${eps27:.2f} vs ${I['consensus_adj_eps_2027']:.2f} "
          f"({eps27/eps26*100-100:+.1f}% growth vs Street {I['consensus_adj_eps_2027']/I['consensus_adj_eps_2026']*100-100:+.1f}%)")
    print(f"  2027 operating income ${oi27:.1f}m vs 2026E ${oi26:.1f}m; net interest ${int27:.1f}m vs ${int26:.1f}m; average adjusted shares {sh27:.2f}m")
    # net debt and shares path (buybacks $50.5m a quarter at today's price)
    nd = 2198.6 - 955.4
    print(f"\nnet debt Sep 2026 ${nd:.1f}m (ATM cash not netted); with buybacks at $202m a year funded from owner earnings of ~${oe['2027']:.0f}m, net debt falls ~${oe['2027']-202:.0f}m in 2027")
    print(f"shares: {I['basic_shares_m']:.2f}m today; $202m a year at ${P} retires {202/P:.2f}m a year")
    open(os.path.join(OUT, 'model_value.txt'), 'w').write(f"{v:.2f}\n")

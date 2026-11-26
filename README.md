# eeft-owner-earnings

Data and code behind my Seeking Alpha piece on Euronet Worldwide (EEFT), "Euronet: Take Out The Buybacks And The Street Still Needs 6% Profit Growth" (November 2026). SELL over 12 months, low conviction, value $65.57 (probability-weighted $66.48) from $69.07. My Q4 2026 forecasts are in results/eeft_live_model.xlsx and get scored after the print.

The whole call rests on owner earnings, so I wanted it checkable. Owner earnings here are GAAP net income plus depreciation and amortization, less capex. I leave share comp in as a cost and I don't use the company's adjusted EPS.

## How to run

Python 3. Most scripts need nothing extra; build_live_model_xlsx.py and export_model_xlsx.py need openpyxl, and price_index.py needs playwright unless you run it with --ria-from-file. Each script finds its data relative to itself, so run them from any folder:

    python scripts/owner_earnings.py
    python scripts/segments_ttm.py
    python scripts/corecard_clock.py
    python scripts/valuation.py
    python scripts/sum_of_parts.py
    python scripts/model.py
    python scripts/export_model_xlsx.py
    python scripts/implied_move.py
    python scripts/price_index.py --ria-from-file
    python scripts/price_index_summary.py
    python scripts/legacy_pi.py
    python scripts/sensitivity.py
    python scripts/consensus_bridge.py
    python scripts/price_check.py
    python scripts/trend_test.py
    python scripts/corecard_deal.py
    python scripts/tieout.py

Run owner_earnings.py first, the others read its output.

## What each script gives you

- owner_earnings.py: owner earnings for 2023, 2024, 2025 and the twelve months to September 2026 ($314.2m), per share, and the 12.4% yield on the market cap.
- segments_ttm.py: twelve-month operating income by segment ($280.5m, $144.3m, $159.7m, corporate -$102.8m) and the 27.3% cross-border share.
- corecard_clock.py: the Apple Card clock. Euronet's $40.2m single-customer intangible over 2.4 years runs out around March 2028; Chase's ~24-month transition from 7 Jan 2026 lands around January 2028. It also checks the $4.75m a quarter of purchase amortization against the $4.7m in the Q3 release, and sizes the cliff at $17.7m a year after tax.
- valuation.py: the growth rate the price implies (-2.1% a year at 10%), the value grid, the $80.71 target on base owner earnings of $296.5m and what's left for Ria at $69.07 ($16.75 a share, 5.9x after-tax profit).
- sum_of_parts.py: each segment at a listed peer's forward EV/EBITDA (NCR Atleos 6.53x, Western Union 4.75x, 6.0x for epay), giving $71.43 a share with the ATM cash left in, $96.27 with it netted. Also the pre-tax return on segment assets (8.9%, 16.0%, 9.6%).
- model.py: the call. Quarterly segments Q4 2026 to Q4 2028, years to 2030, interest on the CME SOFR futures curve, terminal value after the $1bn convertible is refinanced in Oct 2030 at the revolver rate on the 2030 forward, owner earnings, value ($65.57), sensitivities, my Q4 2026 forecast and my adjusted EPS vs consensus. Every assumption is a named variable at the top.
- export_model_xlsx.py: writes the model to results/eeft_model.xlsx (values only, kept for the record).
- build_live_model_xlsx.py: writes results/eeft_live_model.xlsx, the same model with every calculated cell as an Excel formula off the Inputs sheet (blue cells). Value per share $65.57 on the Valuation sheet. Type the actual Ria Q4 print into ria_q4_print and 2027 re-bases. The Monitor sheet lists the five series that decide the call and when they come out; results/EEFT-monitor-2026-11-26.pdf is the same page as a one-pager.
- playbook.py: what each Ria Q4 print does to the value. $42m gives $68.80 (still SELL), $33m gives $62.42, and Ria needs $46.6m on its own, or $39.6m with 2% growth after, to reach the $72.07 HOLD line.
- sga_split.py: Ria's Q3 SG&A increase of $10.1m split into the ~$6m of incremental advertising management named on the Q3 call and ~$4.1m of everything else, including professional fees. Value if the advertising reverses: $69.80; the rest: $68.46; both: $72.69.
- what_is_priced.py: how EEFT traded on its last eight reports (four misses, all down on the day, average -5.3%; beats +1.3%), where the 2027 Street sits (9 analysts, $11.50 to $11.89, down 4.7% over six months, flat over one), and the probability-weighted value: bear $60.02, base $65.57, bull $74.77, 25/50/25 = $66.48 (-3.7%).
- street_bridge.py: the consensus bridge. $10.55 (2026) to $11.63 (2027): buybacks all year +$0.70 (average shares 38.76m to 36.36m), higher interest on the SOFR curve -$0.30, leaving $0.67 a share, $24.5m of adjusted earnings, $32.6m more operating income than the Street's 2026 (+6.4%). Mine is -3.1%; the gap in 2027 operating income is $68.7m.
- banxico_by_state.py: remittances to Mexico by US state, Q3 2026 vs Q3 2025 (Banxico SIE CE168): total +0.8%, Arizona -9.9%, Florida -2.7%, Texas -2.6%, Georgia -1.9%, California +1.1%, Illinois +1.9%, New York +4.6%.
- build_live_model_xlsx.py also writes a Street bridge sheet and a simplified 3-Statement sheet (income, cash flow, balance sheet from 30 Sep 2026; debt is the plug with cash held flat; the balance check is zero every year).
- ria_cost_bridge.py: Ria's Q3 operating income, 2025 to 2026, line by line from the 10-Q: gross profit -$12.8m, salaries +$0.6m, SG&A -$10.1m (up 17%), D&A +$0.3m = -$22.0m. SG&A by quarter (+$7.1m, +$5.8m, +$10.1m) and the value if the step-up reverses ($72.69 for Q3's, $70.99 for the average) or keeps going (+$5m a quarter: $62.04).
- revenue_per_transfer.py: revenue per transfer $9.83 to $9.51 (-3.3%, -2.8% in constant currency), split into the shift to digital (-1.6 points if a digital transfer earns two-thirds of a walk-in one, from my Mexico price check) and the rest (-1.2 points), with the split at 50% and 80% too.
- price_weighted.py: Ria's bank-funded price gap weighted by 2025 remittance inflows (World Bank). Across Mexico, Guatemala and Honduras Ria is $0.46 dearer than the cheapest rival; Mexico alone is +$0.86.
- peer_panel.py: nine months to September. Ria North America revenue -7.5%, Western Union North America money transfer revenue -8.4%, Remitly US-sender revenue +24.5%, Intermex transactions -12.8%, Mexico transfer count -2.7% (Banxico), Ria transfers worldwide -1.3%.
- bull_case.py: the bull case in numbers (TTM owner earnings $314.2m, a 12.4% yield; buybacks retire 2.92m shares a year, 8.0%) and my answer (owner earnings $290.5m in 2027 and $227.3m in 2031, a 9.0% yield on today's price). Also the neutral-inputs value ($74.77 with CoreCard keeping half, Q1 2027 at $41.9m and a 31% tax rate; $77.98 with legacy PI flat too), the BUY line ($78.98) and the Ria Q4 print that reaches it ($56.4m flat, $44.0m with Ria +2% and PI flat), and what a 10% EPS growth guide needs (about $49m to $50m more operating income than my build).
- price_index_compare.py: every run with Ria in it, Ria's bank-funded cost and rank in Mexico, Guatemala, Honduras and El Salvador. The 26 Nov recheck 90 minutes after the first run had the same Ria quotes and ranks. It's a check on the method; the weekly series starts there.
- ria_us_exposure.py: Cross-Border revenue booked in North America, mostly the US sending side. 42.6% of the segment in Q3 2026, down 8.3%; 46.5% in 2024 and 44.9% in 2025; down 4.4%, 7.4% and 8.3% in Q1 to Q3 2026. Everything else -1.9% in Q3.
- count_vs_average.py: remittance growth split into number of transfers and average size (Mexico Jan-Sep: transfers -2.7%, average +5%; Honduras survey average +12.9%), and the EMBI move from end-July to end-October (Guatemala +20bp, Honduras +40bp, El Salvador +42bp).
- ria_agent_tracker.js: run in a normal browser console on Ria's locations page. Samples Ria's US send locations in ten metros from its public locator on a fixed grid. The locator caps each query at about 50 results, so it's a fixed-method sample to compare month to month, not a census. Baseline in data/ria_agent_sample.csv.
- implied_move.py: a rough options-implied move for the Q4 print from the $70 straddles.
- price_index.py: the weekly remittance price index, $400 to ten countries, Ria vs Western Union, Remitly, Xoom and Wise. Ria's site blocks headless cloud browsers, so on those runs I read Ria's calculator in my own browser into data/ria_browser_<date>.csv and run with --ria-from-file.
- price_index_summary.py: where Ria ranks and the cash premium, latest run.
- legacy_pi.py: Payments Infrastructure outside CoreCard by quarter, reported and in constant currency using Euronet's own release percentages. Nine months: -1.8% reported, -0.7% constant currency. Run it before sensitivity.py.
- sensitivity.py (the earlier single-stage version, kept for the record): Base owner earnings $299.2m (TTM $314.2m, less the $17.7m CoreCard cliff, plus $2.7m of growth capex = capex over depreciation), split by segment, central value $78.78, the one-at-a-time swings and the 27-case growth grid ($74.65 to $85.97 for the middle half).
- consensus_bridge.py: Q3 2026 from Euronet's $137.0m of adjusted earnings to my $126.4m of owner earnings, line by line, plus the Street's EPS and P/E.
- price_check.py: the all-in cost of sending $400 to Mexico, Guatemala and India on 26 Nov 2026, Ria's own calculator vs Wise's comparison feed. Inputs are in data/price_check_2026-11-26.
- trend_test.py (earlier version of the call, kept for the record): the call. Splits the $296.5m base by segment and values each at its own growth rate. Flat everywhere is $80.71, Payments Infrastructure shrinking 1.8% with the rest flat is $74.55 (my fair value), and add epay -2% and Ria -3% and it's $64.85. Also prints Ria's quarterly operating income and the +0.5% transfer math.
- corecard_deal.py: what Euronet paid for CoreCard ($192.7m in about 2.55m shares, $150.1m net of CoreCard's cash and investments), the $88.3m of goodwill, the cliff per share ($0.48), the 2025 buyback average ($92.44) and the BUY and SELL prices.
- tieout.py: asserts the segment totals and the owner earnings tie to the filings.

## Sources

- Western Union Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1365135/000119312526447662/wu-20260930.htm
- Remitly Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1782170/000162828026070142/rely-20260930.htm
- Intermex Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1683695/000162828026072217/imxi-20260930.htm
- Banxico Jan-Sep 2026 transfers and average, as reported by Publimetro (3 Nov 2026): https://www.publimetro.com.mx/noticias/2026/11/03/remesas-mexico-peor-nivel-empleo-mexicanos-estados-unidos/
- BCH sender survey, August 2026, via El Heraldo: https://www.elheraldo.hn/economia/monto-de-remesas-que-hondurenos-envian-sube-de-45180-a-51030-al-mes-EB32225735
- EMBI end-October 2026, Bloomberg Linea (3 Nov 2026): https://bloomberglinea.com/latinoamerica/asi-se-me-movio-el-riesgo-pais-en-america-latina-en-octubre-fuerte-alza-en-argentina-y-ecuador/
- Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1029199/000155485526002297/eeft-20260930.htm
- FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1029199/000155485526000131/eeft-20251231.htm
- Q3 2026 release: https://ir.euronetworldwide.com/node/22846/pdf
- SEC XBRL company facts for the 2023 and 2024 cash flow lines: https://data.sec.gov/api/xbrl/companyfacts/CIK0001029199.json
- IRS on the remittance tax: https://www.irs.gov/newsroom/treasury-irs-issue-proposed-regulations-on-the-new-remittance-transfer-tax-established-under-the-one-big-beautiful-bill
- Banco de Guatemala remittances: https://www.banguat.gob.gt/sites/default/files/banguat/estaeco/remesas/remfam2002_2026.htm
- BCR El Salvador remittances: https://estadisticas.bcr.gob.sv/serie/ingresos-mensuales-de-remesas-familiares
- Western Union Q3 2026 release: http://s21.q4cdn.com/100551446/files/content_files/3Q26-Press-Release-FINAL.pdf
- ECB SPACE 2024: https://www.ecb.europa.eu/stats/ecb_surveys/space/shared/pdf/ecb.space2024~19d46f0f17.en.pdf
- CoreCard 10-K FY2024: https://www.sec.gov/Archives/edgar/data/320340/000143774925005708/ins20241231_10k.htm
- Goldman Sachs on the Apple Card transition: https://www.goldmansachs.com/pressroom/press-releases/2026/goldman-sachs-announces-agreement-to-transition-apple-card-program-to-chase
- Euronet Q1 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1029199/000155485526000931/eeft-20260331.htm
- Euronet Q3 2025 10-Q: https://www.sec.gov/Archives/edgar/data/1029199/000155485525001937/eeft-20250930.htm
- El Salvador Jan-Sep 2026 (BCR, via El Mundo): https://diario.elmundo.sv/economia/hogares-salvadorenos-captaron-7619-9-millones-en-remesas-al-tercer-trimestre
- Euronet Q1, Q2, Q3 2026 earnings releases (8-K exhibit 99.1): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001029199&type=8-K
- Ria calculator: https://www.riamoneytransfer.com/en-us/send-money-to-mexico/
- Wise comparison feed: https://api.wise.com/v4/comparisons/?sourceCurrency=USD&targetCurrency=MXN&sendAmount=400
- EU Regulation 2019/518: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0518
- FRED BBB yield: https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY
- FRED SOFR: https://fred.stlouisfed.org/series/SOFR
- CME 3-month SOFR futures settlements: https://www.cmegroup.com/markets/interest-rates/stirs/three-month-sofr.settlements.html
- World Bank WDI API: https://api.worldbank.org/v2/country/GTM;SLV;HND;MEX/indicator/BX.TRF.PWKR.DT.GD.ZS?format=json
- BCH remittances via La Tribuna: https://www.latribuna.hn/2026/10/22/remesas-a-honduras-crecen-112-en-el-tercer-trimestre-y-suman-10-098-millones-de-dolares/
- Q4 2025 release (restructuring charge): https://www.sec.gov/Archives/edgar/data/1029199/000155485526000072/
- Nasdaq option chain and institutional holdings: https://www.nasdaq.com/market-activity/stocks/eeft
- Damodaran's inputs: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm

## Things to be careful with

- The twelve-month figures are full-year 2025 minus nine months of 2025 plus nine months of 2026. Q4 is seasonal for epay and Q3 for the ATMs, so a single quarter times four would be wrong.
- The 10-K segment table uses the old names (EFT Processing, Money Transfer). They're the same segments as Payments Infrastructure and Cross-Border Payments.
- Peer multiples are Seeking Alpha's forward EV/EBITDA on 26 Nov 2026. epay has no clean listed peer, so 6.0x is my judgement.
- The 34.7% tax rate is the 9M 2026 effective rate. Using a lower statutory rate would make the cross-border after-tax profit bigger and Ria look even cheaper.
- Q4 2025 Cross-Border operating income of $37.2m includes a $20.4m restructuring charge; adjusted it was $57.6m. My earlier drafts missed this.
- Euronet has no straight bonds, and the convertible's 89.7% price includes the conversion option, so I refinance at the revolver's all-in rate on the 2030 forward. The BBB index (6.09%) is the high case.
- Tax: cash taxes paid ($155.8m TTM) are close to GAAP tax ($160.8m), so I use the 34.7% nine-month rate. The US is loss-making ($100.4m pre-tax loss in 2025), so the 25% shield on interest may not show up in cash; with no shield the value is $60.22.
- The 2025 'non-cash GAAP tax expense' of $42.4m in the full-year reconciliation doesn't match the quarters (-$2.0m); with the line next to it, both total about -$21.6m. See data/findings_2026-11-26.csv.
- Ria Q1 2027 uses Q1's share of Q2+Q3 in 2024 and 2025 (35.3%, 36.1%) applied to 2026. Holding Q1 at $41.9m instead gives $67.88.
- Floating debt (revolver $689.1m plus uncommitted lines $445.7m) is repriced on CME 3-month SOFR futures settled 25 Nov 2026. The 10-Q says revolver interest at 30 Sep 2026 was based on SOFR; it only says the uncommitted lines are variable. Leaving them off the curve adds $0.33.
- Interest tax shield: 25% (federal plus state). The 10-K lists foreign and state loss carryforwards but no federal ones, so the US deductions are being used; 21% gives $64.43.
- The convertible is refinanced at the revolver's all-in rate on the 2030 forward (5.54%).
- North America revenue is a proxy for US-originated business. It includes Canada and Xe, and Euronet doesn't split profit by region, so the US share of Ria's profit could differ from 42.6%.
- Mexico's count and average are Banxico's as reported by Publimetro; Honduras's average comes from a BCH sender survey, which isn't the same thing as a transaction count.
- The playbook re-bases all of 2027 by the ratio of the Q4 print to my $37.44m forecast. A print that's a one-off (a timing item, a restructuring credit) would overstate the change.
- The Q4 ranges are my judgement at roughly 70% odds each, not a statistical interval. They aren't independent: EPS moves with Ria.
- The 26 Nov recheck read Ria's calculator by hand for four corridors (bank-funded only) and is saved as data/ria_browser_2026-11-26-recheck.csv; price_index.py --ria-from-file uses the alphabetically last ria_browser file, so rename or pass the file you want if you rerun.
- The digital/walk-in revenue ratio in revenue_per_transfer.py comes from one corridor on one day. Euronet doesn't split revenue that way.
- The peer panel mixes measures: revenue for Ria, Western Union and Remitly, transactions for Intermex. Western Union's North America is by where the transfer starts; Remitly's is US senders only; Ria's includes Canada and Xe.
- The price weights use each country's total remittance inflows. For these four corridors most of the money comes from the US, but not all.
- The SG&A scenarios use ria_add_q in model.py, which adds a fixed amount to every Ria quarter from 2027.
- model.py now counts a full year of buybacks in the 2027 share count (it used half a year before), so my 2027 adjusted EPS is $10.29.
- Banxico's CE168 chart labels each quarter by the previous quarter-end date (Jul-Sep 2026 shows as 30/06/2026). I matched values to the table's quarter headers.
- Borrow cost (data/borrow_2026-11-26.csv) is Interactive Brokers' fee via IBorrowDesk, one broker's view.
- The 3-Statement sheet holds other assets and liabilities flat. It's for the cash and debt path, not a full balance sheet forecast.
- The scenario weights (25/50/25) are my judgement. what_is_priced.py also prints 20/50/30 and 15/50/35.
- The earnings reactions use the 8-K filing date and the prior close; consensus is Seeking Alpha's normalized EPS mean, which may differ slightly from other providers.
- Buyback authorization isn't a constraint: $68.4m left under the June 2025 program plus $425m under the February 2026 program (Q3 10-Q).
- A disclosure quirk in the Q3 2026 10-Q, Cross-Border segment: it says currency "increased direct operating costs by approximately $1.1 million and decreased directs operating costs by $13.8 million for the three and nine months". The Q2 10-Q had currency increasing those costs by $14.8m over six months, and revenue moved the same way in every quarter (+$22.9m Q1, +$6.6m Q2, -$2.1m Q3; +$27.9m nine months). $14.8m less $1.1m is $13.7m, so the numbers only reconcile if Q3 currency decreased costs by $1.1m and the nine-month effect increased them by $13.8m. I read it as the two verbs swapped, the same direction as revenue, and it doesn't change any figure I use, since I work from Euronet's own constant-currency growth rates.
- The Q3 call's "50% of our total transactions land in a digital account" is the receiving side (payout into accounts). The 17.9% digital share in revenue_per_transfer.py is the sending side (8.1m of 45.3m transfers started digitally). Different measures, both correct.
- The neutral-inputs value is there so you can see how much of the SELL is my input choices. On those inputs it's a HOLD.
- Q4 EPS is the average of two methods: a direct build at the 24.8% nine-month adjusted tax rate ($2.24) and Q3's ratio of adjusted-earnings change to operating-income change ($2.28).
- The macro table (data/macro_receiving_countries.csv) uses World Bank annual data; the 'cash third falls 10%' line assumes the cash share of dollars equals the cash share of households in the IRS proposed rule.
- The Q4 EPS forecast uses Q3's ratio of adjusted earnings change to operating income change (0.48). That's one quarter of evidence.
- Some Wise-feed quotes for other providers are up to two days old, and rates above mid-market (promos) are dropped.
- Constant currency figures are Euronet's, rounded to whole percent, so each quarter carries about half a point of noise. Q3 2026 also has a $1.7m timing item Euronet calls out in its release.
- Growth capex is capex less depreciation. Depreciation understates true maintenance spend when prices rise, so the $2.7m is generous to me.
- The price check is one snapshot on one day. Wise collects its competitors' quotes itself and doesn't say how they were funded. Ria's numbers are its standard rate, not the first-transfer promo.
- The segment split of owner earnings is pro rata to operating income, with corporate spread across all three. It's a simplification. The growth rates for epay and Ria in the bear case are my judgement, the -1.8% for Payments Infrastructure is the measured nine-month change outside CoreCard.
- I don't net the $912.7m of ATM cash against debt. The machines need it.
- The cost of equity is my judgement: Damodaran's 4.94% risk-free and 4.41% premium with a beta of 1.0 gives 9.35%, and I use 10%. My rating bands are BUY above 14.35% expected return and SELL below 4.35%.

- The CoreCard cliff takes out all of CoreCard's operating income because half its revenue at a 60.3% gross margin is more than its profit. I give zero to new CoreCard clients and to any termination payment from Goldman.

## Corrections

None so far.

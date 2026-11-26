# The Apple Card clock inside Payments Infrastructure.
import os, csv, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
c = {r['item']: r['value'] for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'corecard.csv')))}
f = lambda k: float(c[k])
close = dt.date.fromisoformat(c['euronet_close'])
life = f('large_customer_relationship_life_years')
end = close + dt.timedelta(days=round(life * 365.25))
print(f"large customer relationship ${f('large_customer_relationship_m')}m over {life} years from {close}: fully amortized around {end}")
chase = dt.date.fromisoformat(c['chase_announcement']) + dt.timedelta(days=round(24 * 30.44))
print(f"Chase transition at ~24 months from 7 Jan 2026: around {chase}")
ppa_q = (f('large_customer_relationship_m') / life + f('platform_m') / 9 + f('trade_name_m') / 18 + f('other_customers_m') / 18) / 4
print(f"implied purchase-price amortization ${ppa_q:.2f}m a quarter (the Q3 release says a $4.7m increase)")
print(f"Goldman's FY2024 revenue at CoreCard: ${f('corecard_revenue_fy2024_k')*f('goldman_share_fy2024_pct')/100/1000:.1f}m")
rev = f('revenue_9m2026_m') * 12 / 9; oi = f('op_income_9m2026_ex_ppa_m') * 12 / 9
gm = f('gross_margin_9m2026_m') / f('revenue_9m2026_m')
lost_gp = rev / 2 * gm
print(f"CoreCard annualized: revenue ${rev:.1f}m, operating income ${oi:.1f}m, gross margin {gm*100:.1f}%")
print(f"if half the revenue goes (management's words), gross profit lost ${lost_gp:.1f}m, more than the ${oi:.1f}m operating income, so I take the whole ${oi:.1f}m out")
tax = 121.4 / (228.7 + 121.4)
cliff = oi * (1 - tax)
print(f"after tax at {tax*100:.1f}%: ${cliff:.1f}m a year")
open(os.path.join(HERE, '..', 'results', 'corecard_cliff.txt'), 'w').write(f"{cliff:.4f}\n")

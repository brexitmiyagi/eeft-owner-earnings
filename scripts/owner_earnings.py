# Owner earnings = net income + D&A - capex. Share comp stays in as a real cost.
import os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
rows = {r['period']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'annual_cash.csv')))}
def oe(r): return float(r['net_income_m']) + float(r['d_and_a_m']) - float(r['capex_m'])
out = []
for y in ('2023', '2024', '2025'):
    r = rows[y]; v = oe(r); s = float(r['basic_avg_shares']) / 1e6
    out.append((y, v, s, v / s)); print(f"{y}: owner earnings ${v:.1f}m on {s:.2f}m shares = ${v/s:.2f} a share")
ttm = oe(rows['2025']) - oe(rows['9M2025']) + oe(rows['9M2026'])
avg = float(rows['9M2026']['basic_avg_shares']) / 1e6   # 9M 2026 average, same basis as the annual rows
cur = 36.737747                                         # 10-Q cover count, 4 Nov 2026
out.append(('TTM Sep-2026', ttm, avg, ttm / avg))
print(f"TTM to Sep 2026: ${ttm:.1f}m, ${ttm/avg:.2f} a share on the 9M average of {avg:.2f}m shares, ${ttm/cur:.2f} on today's {cur:.2f}m")
price, mcap = 69.07, 2537.5
print(f"owner earnings yield {ttm/mcap*100:.1f}% on a ${mcap:,.1f}m market cap")
with open(os.path.join(HERE, '..', 'results', 'owner_earnings.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['period', 'owner_earnings_m', 'shares_m', 'per_share'])
    for o in out: w.writerow([o[0], round(o[1], 1), round(o[2], 2), round(o[3], 2)])
open(os.path.join(HERE, '..', 'results', 'ttm_owner_earnings.txt'), 'w').write(f"{ttm:.2f}\n")

# How much of Ria (Cross-Border Payments) revenue is booked in North America, which for a
# remittance business is mostly the US sending side. Euronet doesn't split profit this way,
# so revenue share is the best proxy the filings give.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = {r['period']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'cross_border_by_region.csv')))}
f = lambda p, c: float(R[p][c])
for y in ('FY2024', 'FY2025'):
    print(f"{y}: North America ${f(y,'north_america'):.1f}m of ${f(y,'total'):.1f}m = {f(y,'north_america')/f(y,'total')*100:.1f}%")
for q in ('Q1', 'Q2', 'Q3'):
    a, b = f(f'{q} 2026', 'north_america'), f(f'{q} 2025', 'north_america')
    print(f"{q} 2026 North America ${a:.1f}m vs ${b:.1f}m: {a/b*100-100:+.1f}%")
na, tot = f('Q3 2026', 'north_america'), f('Q3 2026', 'total')
rest, rest0 = tot - na, f('Q3 2025', 'total') - f('Q3 2025', 'north_america')
print(f"Q3 2026 share {na/tot*100:.1f}%; everything else ${rest:.1f}m vs ${rest0:.1f}m: {rest/rest0*100-100:+.1f}%")
share = na / tot
print(f"North America -8% a year, rest flat -> segment revenue {share*-0.08*100:+.1f}% a year")

# Q3 2026: from Euronet's adjusted earnings to my owner earnings, line by line (Q3 2026 release and 10-Q).
adj = 137.0
lines = [
 ('take share comp back out (Euronet adds it back)', -16.7),
 ('add the rest of D&A (Euronet adds back only the $9.6m of acquired-intangible amortization)', 39.5 - 9.6),
 ('subtract capex (Q3: 9M $91.3m less H1 $64.6m)', -(91.3 - 64.6)),
 ('keep the FX gain Euronet strips out', 3.3),
 ('keep the investment gain and accrual Euronet strips out', 1.3 + 1.7),
 ('drop the tax add-backs', -(0.5 + 2.9)),
]
x = adj
print(f"Euronet adjusted earnings Q3 2026: ${adj:.1f}m (${adj/38.633852:.2f} on 38.63m adjusted diluted shares)")
for name, v in lines:
    x += v; print(f"  {v:+7.1f}  {name}  -> ${x:.1f}m")
oe = 113.6 + 39.5 - (91.3 - 64.6)
assert abs(x - oe) < 0.05, (x, oe)
print(f"owner earnings Q3 2026: ${oe:.1f}m = net income 113.6 + D&A 39.5 - capex 26.7 (${oe/38.633852:.2f} on the same shares)")
sbc_ttm = 55.1 - 39.8 + 47.2
print(f"TTM share comp ${sbc_ttm:.1f}m = ${sbc_ttm/36.737747:.2f} a share on today's count")
for name, eps in (('2025 actual', 9.61), ('2026 consensus', 10.55375), ('2027 consensus', 11.62889)):
    print(f"  adjusted EPS {name}: ${eps:.2f}; P/E at $69.07 {69.07/eps:.1f}x")
print(f"2027 consensus growth {11.62889/10.55375*100-100:+.1f}%; GAAP EPS consensus 2026 $6.72, 2027 $7.89")
print(f"price / base owner earnings: {69.07*36.737747/299.2:.1f}x")

# Fair value as a range, and which inputs move it most.
# Base owner earnings: TTM $314.2m, less the $17.7m CoreCard cliff, plus growth capex.
# Growth capex = TTM capex less TTM depreciation (XBRL Depreciation and AmortizationOfIntangibleAssets).
import itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
pi_g = round(float(open(os.path.join(HERE, '..', 'results', 'legacy_pi.txt')).read()), 3)   # from legacy_pi.py
shares, price = 36.737747, 69.07
capex_ttm = 125.5 - 93.9 + 91.3                      # 122.9
dep_ttm = (138.5 - 22.2) - (100.8 - 14.2) + (119.4 - 28.9)   # D&A less intangible amortization
growth_capex = max(capex_ttm - dep_ttm, 0)
base = 314.2 - 17.7 + growth_capex
print(f"TTM capex ${capex_ttm:.1f}m vs depreciation ${dep_ttm:.1f}m -> growth capex ${growth_capex:.1f}m; base ${base:.1f}m")
seg = {'PI': 280.5 - 27.1, 'epay': 144.3, 'CB': 159.7}
tot = sum(seg.values())
oe = {k: base * v / tot for k, v in seg.items()}
print('split: ' + ', '.join(f"{k} ${v:.1f}m" for k, v in oe.items()))
def value(k=0.10, g=None, refill=0.0):
    g = g or {}
    v = sum(oe[s] * (1 + g.get(s, 0)) / (k - g.get(s, 0)) for s in oe)
    v += refill * 17.7 / k                              # share of the Apple Card profit replaced, valued flat
    return v / shares
central = dict(k=0.10, g={'PI': pi_g, 'epay': 0.0, 'CB': 0.0}, refill=0.0)
c = value(**central)
print(f"central: ${c:.2f} ({c/price*100-100:+.1f}%)  [PI {pi_g*100:.1f}% (legacy, constant currency, 9M 2026), epay 0%, Ria 0%, no refill, 10%]")
swings = {
 'Cost of equity 11% / 9.35%': [dict(central, k=0.11), dict(central, k=0.0935)],
 'Payments Infrastructure -2% / +1%': [dict(central, g={**central['g'], 'PI': -0.02}), dict(central, g={**central['g'], 'PI': 0.01})],
 'Ria -3% / +2%': [dict(central, g={**central['g'], 'CB': -0.03}), dict(central, g={**central['g'], 'CB': 0.02})],
 'epay -2% / +2%': [dict(central, g={**central['g'], 'epay': -0.02}), dict(central, g={**central['g'], 'epay': 0.02})],
 'CoreCard refill 0% / 50%': [dict(central, refill=0.0), dict(central, refill=0.5)],
}
rows = []
for name, (lo, hi) in swings.items():
    a, b = value(**lo), value(**hi)
    rows.append((name, a, b, b - a))
for name, a, b, w in sorted(rows, key=lambda r: -r[3]):
    print(f"  {name}: ${a:.2f} to ${b:.2f} (width ${w:.2f})")
# grid over the growth ranges at 10%, every combination
vals = sorted(value(g={'PI': p, 'epay': e, 'CB': r}) for p, e, r in itertools.product((-0.02, pi_g, 0.01), (-0.02, 0, 0.02), (-0.03, 0, 0.02)))
n = len(vals)
print(f"27-case growth grid at 10%: min ${vals[0]:.2f}, 25th ${vals[n//4]:.2f}, median ${vals[n//2]:.2f}, 75th ${vals[3*n//4]:.2f}, max ${vals[-1]:.2f}")
print(f"BUY needs ${price*1.1435:.2f}; SELL below ${price*1.0435:.2f}")
open(os.path.join(HERE, '..', 'results', 'sensitivity.txt'), 'w').write(f"central {c:.2f}\n")
print(f"BUY below ${c/1.1435:.2f}, SELL above ${c/1.0435:.2f} on the central value")
print(f"owner earnings yield on the base at ${price}: {base/(price*shares)*100:.1f}%")

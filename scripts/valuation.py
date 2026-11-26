# What $69.07 assumes, and what the business is worth after the Apple Card leaves CoreCard.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ttm = float(open(os.path.join(HERE, '..', 'results', 'ttm_owner_earnings.txt')).read())
cliff = float(open(os.path.join(HERE, '..', 'results', 'corecard_cliff.txt')).read())
oe = ttm - cliff                      # my base: no refill of the Apple revenue, no termination payment
shares, price = 36.737747, 69.07
mcap = price * shares
print(f"TTM owner earnings ${ttm:.1f}m, less the CoreCard cliff ${cliff:.1f}m = base ${oe:.1f}m")
print(f"cost of equity, beta 1.0 on Damodaran's inputs: {4.94 + 1.0*4.41:.2f}% (I value at 10%)")
for label, x in (('TTM', ttm), ('base after the cliff', oe)):
    g = (0.10 * mcap - x) / (mcap + x)
    print(f"{label}: the price implies {g*100:+.1f}% a year forever at 10%")
for k in (0.09, 0.11, 0.12):
    g = (k * mcap - oe) / (mcap + oe); print(f"  base at k={k*100:.0f}%: {g*100:+.1f}%")
print('value per share on the base (rows k, columns g):')
gs = (-0.02, 0.0, 0.02)
for k in (0.09, 0.10, 0.11):
    print(f"  k {k*100:.0f}%: " + '  '.join(f"{g*100:+.0f}% ${oe*(1+g)/(k-g)/shares:.2f}" for g in gs))
target = oe / 0.10 / shares
print(f"target, flat at 10%: ${target:.2f}, {target/price*100-100:+.1f}%")
cb_after = 159.7 * (1 - 121.4 / (228.7 + 121.4))
rest = oe - cb_after
left = mcap - rest / 0.10
print(f"cross-border after tax ${cb_after:.1f}m; the rest ${rest:.1f}m = ${rest/0.10/shares:.2f}/sh at 10x; left for Ria ${left/shares:.2f}/sh, {left/cb_after:.1f}x")
open(os.path.join(HERE, '..', 'results', 'valuation.txt'), 'w').write(f"base_oe {oe:.2f}\ntarget {target:.2f}\n")

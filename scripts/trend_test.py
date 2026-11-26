# Does the BUY survive if the trends I describe keep going? Splits base owner earnings by segment
# (pro rata to TTM operating income after the CoreCard cliff, corporate spread across all three)
# and capitalizes each piece at its own perpetual growth rate.
shares, price = 36.737747, 69.07
base_oe = 296.5
seg = {'Payments Infrastructure ex the Apple Card': 280.5 - 27.1, 'epay': 144.3, 'Cross-Border': 159.7}
tot = sum(seg.values())
oe = {k: base_oe * v / tot for k, v in seg.items()}
for k, v in oe.items(): print(f"{k}: ${v:.1f}m of base owner earnings ({v/base_oe*100:.1f}%)")
def value(g, k=0.10):
    return sum(oe[s] * (1 + g[s]) / (k - g[s]) for s in oe) / shares
scen = {
 'flat everywhere': (0, 0, 0),
 'ATMs keep shrinking 1.8%, rest flat': (-0.018, 0, 0),
 'ATMs -1.8%, epay -2% (Steam), Ria -3%': (-0.018, -0.02, -0.03),
}
buy_line = price * 1.1435
print(f"BUY line: ${buy_line:.2f} (14.35% over ${price})")
for kk in (0.10, 0.0935):
    print(f"cost of equity {kk*100:.2f}%")
    for name, gs in scen.items():
        v = value(dict(zip(oe, gs)), kk)
        print(f"  {name}: ${v:.2f} ({v/price*100-100:+.1f}%)")
flat, bear = value(dict(zip(oe, scen['flat everywhere']))), value(dict(zip(oe, scen['ATMs -1.8%, epay -2% (Steam), Ria -3%'])))
p = (buy_line - bear) / (flat - bear)
print(f"odds on 'flat' needed for a BUY at 10%: {p*100:.0f}%")
# Ria quarterly operating income, $m (10-Qs and 10-Ks; Q4 = full year less nine months)
q = {'Q4 2024': 201.0-142.6, 'Q1 2025': 45.1, 'Q2 2025': 170.0-59.3-45.1, 'Q3 2025': 59.3, 'Q4 2025': 207.2-170.0,
     'Q1 2026': 41.9, 'Q2 2026': 122.5-37.3-41.9, 'Q3 2026': 37.3}
for k_, v in q.items(): print(f"  Cross-Border op income {k_}: ${v:.1f}m")
print(f"TTM check: {q['Q4 2025']+q['Q1 2026']+q['Q2 2026']+q['Q3 2026']:.1f}")
# next year's transfer count if Q3 rates hold: digital 17.9% of transfers growing 34%, the rest falling 6.8%
d = 8.1/45.3
print(f"digital share {d*100:.1f}%; next-year transfers at Q3 rates: {(d*1.34 + (1-d)*0.932 - 1)*100:+.1f}%")

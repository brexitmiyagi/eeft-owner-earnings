# Splits Ria's Q3 fall in revenue per transfer into currency, mix (more digital) and the rest.
# The mix step needs one assumption: what a digital transfer earns against a walk-in one. I take it
# from my own price check, Mexico $400: bank-funded fee + FX margin vs cash-funded (tax excluded).
HERE = None
rev25, rev26, fx26 = 452.4, 431.0, -2.1          # Q3 10-Q; currency cut 2026 revenue by $2.1m
t25, t26 = 46.0, 45.3
d25, d26 = 6.1, 8.1                               # digital transfers, Q3 10-Q / release
rpt25, rpt26 = rev25 / t25, rev26 / t26
rpt26cc = (rev26 - fx26) / t26
print(f"revenue per transfer ${rpt25:.2f} -> ${rpt26:.2f} ({rpt26/rpt25*100-100:+.1f}%); constant currency ${rpt26cc:.2f} ({rpt26cc/rpt25*100-100:+.1f}%)")
bank, fee_bank, fee_cash = 9.95, 1.99, 7.00       # Ria MX $400, 26 Nov: all-in cost bank-funded, fees
k = bank / (bank - fee_bank + fee_cash)
print(f"a digital transfer earns about {k*100:.0f}% of a walk-in one (Mexico, $400)")
s25, s26 = d25 / t25, d26 / t26
mix = (1 - s26 * (1 - k)) / (1 - s25 * (1 - k)) - 1
print(f"digital share {s25*100:.1f}% -> {s26*100:.1f}%; mix effect {mix*100:+.1f}%; the rest (price, corridor, other) {((1+rpt26cc/rpt25-1)/(1+mix)-1)*100:+.1f}%")
for kk in (0.5, 0.8):
    mx = (1 - s26 * (1 - kk)) / (1 - s25 * (1 - kk)) - 1
    print(f"  if digital earns {kk*100:.0f}%: mix {mx*100:+.1f}%, rest {((rpt26cc/rpt25)/(1+mx)-1)*100:+.1f}%")

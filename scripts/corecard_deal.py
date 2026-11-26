# What Euronet paid for CoreCard, and what the Apple Card loss is worth per share.
# Inputs: Euronet 10-K FY2025 Note 6 (purchase price accounting) and statement of changes in equity.
consideration, shares_issued = 192.7, 2.551683      # $m, millions of shares ("Acquisitions" line, 2025)
cash_in, investments_in, goodwill, big_customer = 33.6, 9.0, 88.3, 40.2
total_goodwill_sep26 = 1018.3                         # XBRL Goodwill, 30 Sep 2026
print(f"paid ${consideration}m in {shares_issued:.2f}m new shares, about ${consideration/shares_issued:.2f} a share")
print(f"net of CoreCard's own cash and investments: ${consideration-cash_in-investments_in:.1f}m")
print(f"goodwill ${goodwill}m = {goodwill/total_goodwill_sep26*100:.1f}% of Euronet's ${total_goodwill_sep26}m")
cliff, shares, price = 17.7, 36.737747, 69.07
print(f"cliff ${cliff}m a year = ${cliff/shares:.2f} a share, ${cliff/shares/0.10:.2f} of value at 10x, {cliff/shares/0.10/price*100:.1f}% of the price")
bought_sh, bought_usd = 7.243649, 669.6               # 2025 repurchases incl. taxes
print(f"2025 buybacks: {bought_sh:.2f}m shares for ${bought_usd}m, average ${bought_usd/bought_sh:.2f}")
print(f"2026 nine-month buybacks: ${101.0+50.5+50.5:.1f}m")
mcap = price*shares
print(f"base owner earnings yield at ${price}: {296.5/mcap*100:.1f}%")
fair = 74.55
print(f"BUY below ${fair/1.1435:.2f}; SELL above ${fair/1.0435:.2f}; at ${price} expected {fair/price*100-100:+.1f}%")
print(f"Q4 2025 vs Q4 2024 cross-border op income: {(207.2-170.0)/(201.0-142.6)*100-100:+.1f}%")
print(f"El Salvador Jan-Sep: {7619.9/7359.0*100-100:+.1f}%")

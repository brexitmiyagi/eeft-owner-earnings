# Rough options-implied move for the Q4 print from the $70 straddles (mid of bid/ask; spreads are wide, so treat as +/- a few points).
import math
S = 69.07
feb = ((4.20 + 5.40) / 2 + (3.90 + 6.70) / 2) / S        # to 19 Feb 2027, 85 days, includes the print
jan = ((1.50 + 4.40) / 2 + (2.30 + 6.10) / 2) / S        # to 15 Jan 2027, 50 days, before the print
var_day = jan ** 2 / 50
earn = math.sqrt(max(feb ** 2 - var_day * 85, 0))
print(f"Feb straddle {feb*100:.1f}% of price, Jan {jan*100:.1f}%; implied move for the print about +/-{earn*100:.1f}%")
print("last two prints: -7.0% (31 Jul 2026) and -7.7% (27 Oct 2026)")

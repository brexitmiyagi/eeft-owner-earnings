# The Street's bridge, not mine: from the $10.55 consensus for 2026 to $11.63 for 2027, how much
# comes from buybacks, how much interest takes away on the SOFR futures curve, and what operating
# income growth is left over. Adjusted earnings = EPS x adjusted diluted shares, as Euronet reports.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as m
I = m.I
P = I['price']
c26, c27 = I['consensus_adj_eps_2026'], I['consensus_adj_eps_2027']
q_earn = 62.6 + 110.0 + 137.0                       # adjusted earnings Q1-Q3 2026, releases
q_eps = I['adj_eps_q1_2026'] + I['adj_eps_q2_2026'] + I['adj_eps_q3_2026']
sh_q3 = I['adj_diluted_shares_q3_m']
bb_q = I['buyback_per_quarter_m'] / P               # shares retired a quarter at today's price
sh_q4 = sh_q3 - 0.45                                # same Q4 share count as model.py
street_q4 = c26 - q_eps
e26 = q_earn + street_q4 * sh_q4                    # Street-implied 2026 adjusted earnings
sh26 = e26 / c26                                    # implied average share count behind the $10.55
# 2027 with buybacks every quarter at the same pace: average of four quarterly averages
sh27 = sum(sh_q4 - bb_q * (i + 1) for i in range(4)) / 4   # model.py uses the same full-year pace
print(f"Street 2026: adjusted earnings ${e26:.1f}m (Q4 at ${street_q4:.2f} x {sh_q4:.2f}m), implied average shares {sh26:.2f}m")
print(f"2027 average shares with buybacks all year at ${4*I['buyback_per_quarter_m']:.0f}m: {sh27:.2f}m ({sh27/sh26*100-100:+.1f}%)")
step1 = c26 * sh26 / sh27
print(f"1) buybacks alone: ${c26:.2f} -> ${step1:.2f} ({step1/c26*100-100:+.1f}%)")
int26 = (14.1 - 4.1) + (20.6 - 4.8) + (21.7 - 5.0) + (I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m'])
int27 = (I['interest_exp_q3_2026_m'] - I['interest_inc_q3_2026_m']) * 4 + m.FLOATING_DEBT * (m.SOFR_YEAR['2027'] - I['sofr_2026_11_24'])
d_int_at = -(int27 - int26) * (1 - 0.25)
step2 = step1 + d_int_at / sh27
print(f"2) net interest ${int26:.1f}m -> ${int27:.1f}m on the futures curve: {d_int_at:+.1f}m after tax, ${d_int_at/sh27:+.2f} -> ${step2:.2f}")
# if the buybacks are funded with revolver debt instead of cash flow
bb_int = 4 * I['buyback_per_quarter_m'] * 0.5 * (m.SOFR_YEAR['2027'] + 0.0125) * (1 - 0.25)
print(f"   (if the buybacks were all borrowed, another -${bb_int:.1f}m after tax, ${-bb_int/sh27:.2f})")
resid = (c27 - step2) * sh27
adj_rate = 102.2 / 412.0
oi_need = resid / (1 - adj_rate)
print(f"3) left for operations: ${c27 - step2:.2f} a share = ${resid:.1f}m of adjusted earnings = ${oi_need:.1f}m more operating income than 2026 at the 24.8% adjusted tax rate")
# Street 2026 operating income: my 2026 plus what its Q4 needs
v, rows, years, oe, *_ = m.run(verbose=True)
q4 = rows[0]
oi26_mine = 72.0 + 137.1 + 171.6 + q4['oi']
per_dollar = ((I['adj_earnings_q3_2025_m'] - I['adj_earnings_q3_2026_m']) / 23.4 + (1 - adj_rate)) / 2
oi26_street = oi26_mine + (street_q4 - 2.26) * sh_q4 / per_dollar
oi27_street = oi26_street + oi_need
print(f"Street-implied operating income: 2026 ${oi26_street:.1f}m, 2027 ${oi27_street:.1f}m ({oi_need/oi26_street*100:+.1f}%)")
print(f"mine: 2026 ${oi26_mine:.1f}m, 2027 ${years['2027']['oi']:.1f}m ({years['2027']['oi']/oi26_mine*100-100:+.1f}%)")
print(f"gap in 2027 operating income: ${oi27_street - years['2027']['oi']:.1f}m")


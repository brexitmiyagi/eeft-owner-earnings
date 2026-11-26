# The Q4 playbook: what each Ria print does to the value. A Q4 print different from my
# $37.4m forecast re-bases 2027 by the same ratio (ria_scale), then I try flat, +2% and -3%.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as m
B = m.I['ria_q4_2025_adjusted_oi_m']
HOLD = 72.07
v = lambda x, g=0.0: m.run(ria_q4=x / B - 1, ria_scale=x / (B * 0.65), g_ria=g)
for x in (33.0, 37.4, 42.0, 45.0):
    print(f"Ria Q4 ${x:.1f}m: flat ${v(x):.2f}, +2%/yr ${v(x,0.02):.2f}, -3%/yr ${v(x,-0.03):.2f}")
def breakeven(g):
    lo, hi = 30.0, 70.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if v(mid, g) < HOLD else (lo, mid)
    return hi
print(f"Ria Q4 needed for HOLD (${HOLD}): flat ${breakeven(0.0):.1f}m, with 2% growth ${breakeven(0.02):.1f}m")
print(f"Legacy PI +1%/yr with Ria at forecast: ${m.run(g_pi=0.01):.2f}")

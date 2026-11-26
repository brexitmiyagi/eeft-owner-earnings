# The bull case in numbers, my answer to it, the neutral-inputs value, the BUY trigger and what a
# 10%-growth 2027 guide would need. Everything comes from model.py so it moves with the model.
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as m
I = m.I
price, sh = I['price'], I['basic_shares_m']
mcap = price * sh
oe_ttm = 314.2                      # owner_earnings.py, twelve months to Sep 2026
print(f"market cap ${mcap:.1f}m; TTM owner earnings ${oe_ttm}m = {oe_ttm/mcap*100:.1f}% yield")
bb = 4 * I['buyback_per_quarter_m']
print(f"buybacks ${bb:.0f}m a year at ${price} retire {bb/price:.2f}m shares = {bb/price/sh*100:.1f}% of {sh:.2f}m")
v, rows, years, oe, oe31, g_t, tv, pv, oe_q4, refi_extra = m.run(verbose=True)
for y in ('2027', '2028', '2029', '2030'):
    print(f"owner earnings {y} ${oe[y]:.1f}m = {oe[y]/mcap*100:.1f}% of today's market cap")
print(f"owner earnings 2031 ${oe31:.1f}m = {oe31/mcap*100:.1f}%, growing {g_t*100:.2f}% a year, against a 10% cost of equity")
print(f"drop from TTM to 2031: ${oe_ttm-oe31:.1f}m")
# neutral inputs, one at a time and together
cases = [('central', {}), ('CoreCard keeps half', dict(corecard_loss=13.55)), ('Ria Q1 2027 holds at $41.9m', dict(ria_q1_27=41.9)),
         ('operating tax 31%', dict(tax_op=0.31)), ('legacy PI flat', dict(g_pi=0.0)), ('convertible refinanced at today SOFR curve 2027 avg', dict(refi=m.SOFR_YEAR['2027'] + 0.0125))]
for n, kw in cases:
    print(f"{n}: ${m.run(**kw):.2f}")
neutral = dict(corecard_loss=13.55, ria_q1_27=41.9, tax_op=0.31)
print(f"neutral inputs (CoreCard half, Q1 at $41.9m, tax 31%): ${m.run(**neutral):.2f}")
print(f"neutral + legacy PI flat: ${m.run(**neutral, g_pi=0.0):.2f}")
buy = price * 1.1435
print(f"BUY needs a value of ${buy:.2f} (expected return 14.35%)")
B = I['ria_q4_2025_adjusted_oi_m']
lo, hi = 30.0, 120.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if m.run(ria_q4=mid / B - 1, ria_scale=mid / (B * 0.65)) < buy else (lo, mid)
print(f"Ria Q4 print that gets to BUY with no growth after: ${hi:.1f}m")
lo, hi = 30.0, 120.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if m.run(ria_q4=mid / B - 1, ria_scale=mid / (B * 0.65), g_ria=0.02, g_pi=0.0) < buy else (lo, mid)
print(f"... with Ria +2% a year and legacy PI flat: ${hi:.1f}m")
# what a 10% EPS growth guide needs, from model.py's own 2026E and 2027E
txt = os.popen(f'{sys.executable} "{os.path.join(HERE, "model.py")}"').read()
e26, e27 = [float(x) for x in re.search(r"2026E \$([\d.]+) vs .*?2027E \$([\d.]+)", txt).groups()]
sh27 = float(re.search(r"average adjusted shares ([\d.]+)m", txt).group(1))
for g in (0.10, I['consensus_adj_eps_2027'] / I['consensus_adj_eps_2026'] - 1):
    need = (e26 * (1 + g) - e27) * sh27
    print(f"2027 EPS growth {g*100:.1f}% needs ${need:.1f}m more adjusted earnings than my build = ${need/0.75:.1f}m more operating income pre-tax (at 25%)")
ria27 = sum(r['ria'] for r in rows if r['period'].endswith('2027'))
print(f"my Ria 2027 ${ria27:.1f}m; Ria 2025 adjusted: 45.1 + 65.6 + 59.3 + 57.6 = ${45.1+65.6+59.3+57.6:.1f}m")
# Q4 EPS: what the consensus needs
street_q4 = I['consensus_adj_eps_2026'] - (I['adj_eps_q1_2026'] + I['adj_eps_q2_2026'] + I['adj_eps_q3_2026'])
print(f"Street implied Q4 ${street_q4:.2f} vs my $2.26 and the top of my range $2.45: gap ${street_q4-2.26:.2f} = ${ (street_q4-2.26)*(I['adj_diluted_shares_q3_m']-0.45):.1f}m of adjusted earnings")
# What Ria alone would need in Q4 for the Street's $2.60, using model.py's own Q4 EPS method
# (average of Q3 pass-through and the direct build: each $1 of operating income adds the average of the two)
pt = (I['adj_earnings_q3_2025_m'] - I['adj_earnings_q3_2026_m']) / 23.4
direct = 1 - 102.2 / 412.0
per_dollar = (pt + direct) / 2
sh_q4 = I['adj_diluted_shares_q3_m'] - 0.45
need_oi = (street_q4 - 2.26) * sh_q4 / per_dollar
print(f"each $1m of Q4 operating income adds ${per_dollar:.3f}m of adjusted earnings; $2.60 needs ${need_oi:.1f}m more, i.e. Ria about ${37.44+need_oi:.1f}m vs $57.6m in Q4 2025")
print(f"value at a 9.35% cost of equity: ${m.run(k=0.0935):.2f}")

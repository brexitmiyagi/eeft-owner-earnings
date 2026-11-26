# What the price already assumes: how EEFT traded on its last eight reports, where the Street's
# estimates sit and which way they're moving, and a probability-weighted value from my scenarios.
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.path.join(HERE, '..', 'data')
beats, misses = [], []
for r in csv.DictReader(open(os.path.join(D, 'earnings_reactions.csv'))):
    a, c = float(r['adj_eps_actual']), float(r['consensus_mean'])
    d1 = float(r['close_release_day']) / float(r['close_day_before']) - 1
    d2 = float(r['close_next_day']) / float(r['close_day_before']) - 1
    tag = 'beat' if a > c else 'miss'
    (beats if a > c else misses).append(d1)
    print(f"{r['quarter']}: ${a:.2f} vs ${c:.2f} ({(a/c-1)*100:+.1f}%, {tag}); release day {d1*100:+.1f}%, two days {d2*100:+.1f}%")
avg = lambda x: sum(x) / len(x) * 100
print(f"misses {len(misses)}: average release-day move {avg(misses):+.1f}%, all down: {all(m < 0 for m in misses)}")
print(f"beats {len(beats)}: average release-day move {avg(beats):+.1f}%")
S = {r['item']: r['value'] for r in csv.DictReader(open(os.path.join(D, 'street_estimates_2026-11-26.csv')))}
print(f"2027: {S['analysts_2027']} analysts, ${S['eps_2027_low']} to ${S['eps_2027_high']}, mean ${float(S['eps_2027_mean']):.2f}; trend 1M {S['eps_2027_trend_1m_pct']}%, 3M {S['eps_2027_trend_3m_pct']}%, 6M {S['eps_2027_trend_6m_pct']}%")
print(f"   six months ago the 2027 mean was about ${float(S['eps_2027_mean'])/(1+float(S['eps_2027_trend_6m_pct'])/100):.2f}; my $10.29 is ${float(S['eps_2027_low'])-10.29:.2f} below the lowest estimate")
import model as m
P = m.I['price']
bear, base, bull = m.run(g_ria=-0.03), m.run(), m.run(corecard_loss=13.55, ria_q1_27=41.9, tax_op=0.31)
w = (0.25, 0.5, 0.25)
ev = w[0] * bear + w[1] * base + w[2] * bull
print(f"bear (Ria -3% a year) ${bear:.2f} ({bear/P*100-100:+.1f}%), base ${base:.2f} ({base/P*100-100:+.1f}%), bull (neutral inputs) ${bull:.2f} ({bull/P*100-100:+.1f}%)")
print(f"25/50/25 expected value ${ev:.2f} ({ev/P*100-100:+.1f}%)")
for ww in ((0.2, 0.5, 0.3), (0.15, 0.5, 0.35)):
    e = ww[0] * bear + ww[1] * base + ww[2] * bull
    print(f"  weights {ww}: ${e:.2f} ({e/P*100-100:+.1f}%)")

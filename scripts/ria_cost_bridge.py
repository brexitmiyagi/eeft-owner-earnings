# Walks Ria's (Cross-Border Payments) Q3 operating income from 2025 to 2026 line by line, and
# shows SG&A by quarter. Then what the model says if the SG&A step-up reverses or keeps going.
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
R = {r['quarter']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'ria_segment_costs.csv')))}
f = lambda q, c: float(R[q][c])
a, b = 'Q3 2025', 'Q3 2026'
gp = lambda q: f(q, 'revenue') - f(q, 'direct_operating_costs')
print(f"revenue {f(b,'revenue')-f(a,'revenue'):+.1f}, direct costs {f(b,'direct_operating_costs')-f(a,'direct_operating_costs'):+.1f}, gross profit {gp(b)-gp(a):+.1f}")
for c in ('salaries', 'sga', 'da'):
    print(f"{c} {f(b,c)-f(a,c):+.1f} (effect on operating income {-(f(b,c)-f(a,c)):+.1f})")
oi = gp(b) - gp(a) - sum(f(b, c) - f(a, c) for c in ('salaries', 'sga', 'da'))
print(f"operating income {oi:+.1f} (reported {f(b,'operating_income')-f(a,'operating_income'):+.1f})")
print(f"gross margin {gp(a)/f(a,'revenue')*100:.1f}% -> {gp(b)/f(b,'revenue')*100:.1f}%; SG&A % of revenue {f(a,'sga')/f(a,'revenue')*100:.1f}% -> {f(b,'sga')/f(b,'revenue')*100:.1f}%")
ups = []
for q in ('Q1', 'Q2', 'Q3'):
    d = f(f'{q} 2026', 'sga') - f(f'{q} 2025', 'sga'); ups.append(d)
    print(f"{q} SG&A ${f(f'{q} 2026','sga'):.1f}m vs ${f(f'{q} 2025','sga'):.1f}m: {d:+.1f}")
print(f"average 2026 step-up {sum(ups)/3:.1f} a quarter")
import model as m
print(f"value if the Q3 step-up ($10.1m a quarter) reverses from 2027: ${m.run(ria_add_q=10.1):.2f}")
print(f"value if the average step-up ($7.7m) reverses: ${m.run(ria_add_q=7.7):.2f}")
print(f"value if SG&A rises another $5m a quarter: ${m.run(ria_add_q=-5.0):.2f}")

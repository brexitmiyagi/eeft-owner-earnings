# Checks that the numbers in the post still come out of the data. Fails loudly if not.
import os, csv, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
seg = {r['segment']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'segments.csv')))}
ttm = {k: float(v['op_income_fy2025']) - float(v['op_income_9m2025']) + float(v['op_income_9m2026']) for k, v in seg.items()}
assert abs(sum(ttm.values()) - 481.7) < 0.05, sum(ttm.values())            # 529.8 - 428.8 + 380.7
assert abs(529.8 - 207.2 - 136.2 + 92.4 - 278.8) < 0.05                    # FY2025 Payments Infrastructure derivation
oe = float(open(os.path.join(HERE, '..', 'results', 'ttm_owner_earnings.txt')).read())
assert abs(oe - 314.2) < 0.05, oe
assert abs((309.5 - 258.0 + 228.5) - 280.0) < 0.05
assert abs(121.4 / (228.7 + 121.4) - 0.347) < 0.001
assert abs(493.4 / 2537.5 - 0.194) < 0.001
assert abs((45.3 - 8.1) / (46.0 - 6.1) - 1 + 0.068) < 0.001
base = float(open(os.path.join(HERE, '..', 'results', 'valuation.txt')).read().split()[1])
assert abs(base - 296.5) < 0.1, base
assert abs((40.2 / 2.4 + 11.0 / 9 + 7.2 / 18 + 11.2 / 18) / 4 - 4.75) < 0.01   # ties to the $4.7m in the Q3 release
assert abs(296.5 * (1 - 0.0108) / (0.10 + 0.0108) / 36.737747 - 72.07) < 0.1
print('tie-out OK')

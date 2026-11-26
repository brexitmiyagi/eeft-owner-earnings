# Payments Infrastructure profit outside CoreCard, quarter by quarter, reported and in constant currency.
# Constant currency comes from Euronet's own release percentages (rounded to whole numbers, so +/- ~0.5 pt).
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'pi_quarterly.csv'))))
tot_cc = tot_prior = tot_rep = 0
for r in rows:
    pi, prior = float(r['pi_op_income_m']), float(r['prior_year_m'])
    cc_core = float(r['corecard_op_ex_ppa_m']) - float(r['corecard_ppa_m'])   # CoreCard's contribution after its own amortization
    legacy = pi - cc_core
    line = f"{r['quarter']}: segment ${pi:.1f}m, CoreCard ${cc_core:+.2f}m, legacy ${legacy:.2f}m vs ${prior:.1f}m = {legacy/prior*100-100:+.1f}% reported"
    if r['cc_growth_pct_company']:
        fx_drag = (float(r['cc_growth_pct_company']) / 100 - (pi / prior - 1)) * prior   # what currency took off the segment's profit
        legacy_cc = legacy + fx_drag
        line += f", currency took ${fx_drag:.2f}m, legacy constant currency ${legacy_cc:.2f}m = {legacy_cc/prior*100-100:+.1f}%"
        tot_cc += legacy_cc; tot_prior += prior; tot_rep += legacy
    print(line)
print(f"9M 2026 legacy: reported {tot_rep/tot_prior*100-100:+.1f}%, constant currency {tot_cc/tot_prior*100-100:+.1f}%")
open(os.path.join(HERE, '..', 'results', 'legacy_pi.txt'), 'w').write(f"{tot_cc/tot_prior-1:.4f}\n")

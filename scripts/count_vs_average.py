# Splits remittance growth into number of transfers and average size, and the EMBI move.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data')
for r in csv.DictReader(open(os.path.join(D, 'remittance_count_average.csv'))):
    a = float(r['avg_usd']) / float(r['avg_prior_usd']) - 1
    line = f"{r['country']} {r['period']}: average ${r['avg_usd']} vs ${r['avg_prior_usd']} ({a*100:+.1f}%)"
    if r['count_m']:
        c = float(r['count_m']) / float(r['count_prior_m']) - 1
        line += f", transfers {r['count_m']}m vs {r['count_prior_m']}m ({c*100:+.1f}%), value {((1+a)*(1+c)-1)*100:+.1f}%"
    print(line)
print("Honduras total inflows through September +11.2% (BCH via La Tribuna): average send grew faster than the total")
for r in csv.DictReader(open(os.path.join(D, 'embi_spreads.csv'))):
    print(f"{r['country']}: {r['end_july_2026_bp']}bp end-July -> {r['end_october_2026_bp']}bp end-October ({int(r['end_october_2026_bp'])-int(r['end_july_2026_bp']):+d}bp)")

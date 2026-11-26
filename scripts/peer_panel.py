# US-outbound panel, nine months to September: who's growing in the market Ria sends from.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'peer_us_outbound.csv'))):
    if r['value_2025']:
        print(f"{r['company']}: {r['measure']} {float(r['value_2026'])/float(r['value_2025'])*100-100:+.1f}%")
    else:
        print(f"{r['company']}: {r['measure']} {r['value_2026']} ({r['source'].split(': ')[-1]})")

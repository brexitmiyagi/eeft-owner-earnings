# Splits Ria's Q3 SG&A increase into what management called advertising and the rest, and values each
# if it reverses from 2027. Also notes the one legal matter the 10-Q lists for the segment.
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as m
R = {r['item']: float(r['value_m']) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'ria_sga_q3_split.csv')))}
adv, oth = R['incremental_advertising_q3'], R['other_incl_professional_fees_q3']
print(f"SG&A +${R['sga_increase_q3']}m = advertising ${adv}m ({adv/R['sga_increase_q3']*100:.0f}%) + other incl. professional fees ${oth:.1f}m")
print(f"value if the advertising reverses from 2027: ${m.run(ria_add_q=adv):.2f}; if the rest reverses: ${m.run(ria_add_q=oth):.2f}; both: ${m.run(ria_add_q=adv+oth):.2f}; base ${m.run():.2f}")
print(f"only legal matter named for the segment: Italian agent withholding tax, about EUR {R['italy_agent_withholding_tax_eur_m']}m, reasonably possible, not accrued")

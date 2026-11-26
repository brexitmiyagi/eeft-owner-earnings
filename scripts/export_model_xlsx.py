# Writes results/eeft_model.xlsx: assumptions, quarterly segments, annual owner earnings, sensitivities, Q4 forecast.
import csv, os, io, contextlib
from openpyxl import Workbook
from openpyxl.styles import Font
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, HERE)
import model as m
v, rows, years, oe, oe31, g_t, tv, pv, oe_q4, refi_extra = m.run(verbose=True)
wb = Workbook(); ws = wb.active; ws.title = 'Assumptions'
ws.append(['item', 'value', 'source']); [c.__setattr__('font', Font(bold=True)) for c in ws[1]]
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'model_inputs.csv'))): ws.append([r['item'], float(r['value']), r['source']])
for k in ('K', 'G_PI_LEGACY', 'G_EPAY_2027', 'RIA_Q4_YOY', 'RIA_Q1_2027', 'G_RIA_AFTER', 'CORECARD_PRE_PPA_Q', 'CORECARD_LOSS_2028', 'CORP_Q', 'REFI_RATE'):
    ws.append([k, getattr(m, k), 'model.py assumption'])
q = wb.create_sheet('Quarterly'); q.append(['period', 'PI', 'PI legacy', 'CoreCard after PPA', 'epay', 'Ria', 'corporate', 'operating income'])
for r in rows: q.append([r['period']] + [round(r[k], 2) for k in ('pi', 'pi_legacy', 'corecard', 'epay', 'ria', 'corp', 'oi')])
a = wb.create_sheet('Owner earnings'); a.append(['period', 'owner earnings $m'])
a.append(['Q4 2026', round(oe_q4, 1)]); [a.append([y, round(x, 1)]) for y, x in oe.items()]; a.append(['2031 (terminal year)', round(oe31, 1)])
a.append([]); a.append(['terminal growth', round(g_t, 4)]); a.append(['terminal value $m', round(tv, 0)]); a.append(['equity value $m', round(pv, 0)]); a.append(['value per share', round(v, 2)])
s = wb.create_sheet('Sensitivity'); s.append(['case', 'value per share'])
for name, kw in [('central', {}), ('cost of equity 9.35%', dict(k=0.0935)), ('cost of equity 11%', dict(k=0.11)), ('refi BBB 6.09%', dict(refi=m.I['bbb_yield_2026_11_24'])), ('refi 4.5%', dict(refi=0.045)), ('Ria Q1 2027 $41.9m', dict(ria_q1_27=41.9)), ('operating tax 31%', dict(tax_op=0.31)), ('no interest tax shield', dict(tax_int=0.0)),
                 ('no refinancing', dict(refi=m.I['convert_coupon'])), ('Ria -3% after 2027', dict(g_ria=-0.03)), ('Ria +2% after 2027', dict(g_ria=0.02)),
                 ('legacy PI -2%', dict(g_pi=-0.02)), ('legacy PI +1%', dict(g_pi=0.01)), ('dollar 10% stronger', dict(fx=-0.10)), ('dollar 10% weaker', dict(fx=0.10)),
                 ('Ria +2% and PI flat', dict(g_ria=0.02, g_pi=0.0))]:
    s.append([name, round(m.run(**kw), 2)])
f = wb.create_sheet('Q4 2026 forecast')
for r in [['line', 'forecast', 'low', 'high', 'Q4 2025'], ['Ria operating income $m', 37.4, 33, 42, 57.6], ['Legacy PI constant currency $m', 43.8, 41, 46, 44.1],
          ['epay operating income $m', 45.9, 42, 49, 47.3], ['Adjusted EPS $', 2.28, 2.15, 2.45, 2.39]]: f.append(r)
wb.save(os.path.join(HERE, '..', 'results', 'eeft_model.xlsx')); print('saved results/eeft_model.xlsx', round(v, 2))

# What it costs to send $400 from the US on 26 Nov 2026: Ria's own calculator vs Wise's comparison feed.
# Cost = fee + tax + the exchange-rate markup in dollars, against Wise's mid-market rate collected at 17:00 UTC.
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data', 'price_check_2026-11-26')
cur = {'MX': 'MXN', 'GT': 'GTQ', 'IN': 'INR'}
mid, others = {}, {}
for c, ccy in cur.items():
    d = json.load(open(os.path.join(D, f'wise_{ccy}.json')))
    for p in d['providers']:
        for q in p['quotes']:
            if q['isConsideredMidMarketRate']: mid[c] = q['rate']
            if p['alias'] in ('western-union', 'remitly', 'wise') and q['dateCollected'].startswith('2026-11-26'):
                others[(c, p['alias'])] = (q['fee'], q['rate'])
def cost(fee, tax, rate, c): return fee + tax + 400 * (1 - rate / mid[c])
ria = {(r['corridor'], r['payment_method'], r['delivery_method']): r for r in csv.DictReader(open(os.path.join(D, 'ria_calculator.csv')))}
for c in cur:
    print(f"{c} (mid {mid[c]}):")
    for pm in ('BankAccount', 'DebitCard', 'PayNearMe'):
        r = ria[(c, pm, 'BankDeposit')]
        x = cost(float(r['transfer_fee_usd']), float(r['tax_usd']), float(r['exchange_rate']), c)
        print(f"  Ria {pm:11s} to a bank: ${x:.2f} ({x/4:.2f}%), of which tax ${float(r['tax_usd']):.2f}")
    for a in ('western-union', 'remitly', 'wise'):
        if (c, a) in others:
            f, rt = others[(c, a)]; x = cost(f, 0, rt, c)
            print(f"  {a:14s}: ${x:.2f} ({x/4:.2f}%)")

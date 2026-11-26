# Weekly remittance price index: the all-in cost of sending $400 from the US to ten corridors,
# Ria (its own public calculator, loaded in a headless browser) vs Western Union, Remitly, Xoom
# and Wise (Wise's public comparison feed). Appends to data/price_index.csv.
# Run: python scripts/price_index.py   (needs playwright with chromium)
import csv, datetime, json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'price_index.csv')
CORR = {'MX': 'MXN', 'GT': 'GTQ', 'IN': 'INR', 'PH': 'PHP', 'SV': 'USD', 'HN': 'HNL', 'DO': 'DOP', 'CO': 'COP', 'VN': 'VND', 'NG': 'NGN'}
AMT = 400
OTHERS = ('western-union', 'remitly', 'xoom', 'wise')

def wise(ccy):
    url = f"https://api.wise.com/v4/comparisons/?sourceCurrency=USD&targetCurrency={ccy}&sendAmount={AMT}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research script)'})
    return json.load(urllib.request.urlopen(req, timeout=30))

def ria_quotes():
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        hdr = {}
        def grab(req):
            if 'MoneyTransferCalculator/Calculate' in req.url and req.method == 'POST' and 'authorization' in req.headers:
                hdr.update({k: v for k, v in req.headers.items() if k.lower() in ('authorization', 'content-type')})
        pg.on('request', grab)
        pg.goto('https://www.riamoneytransfer.com/en-us/send-money-to-mexico/', wait_until='domcontentloaded', timeout=90000)
        for _ in range(30):
            if hdr: break
            pg.wait_for_timeout(1000)
        if not hdr:
            # the calculator fires on input; nudge it
            try:
                pg.fill('input[type="text"], input[inputmode="decimal"]', '401', timeout=10000)
                pg.wait_for_timeout(4000)
            except Exception:
                pass
        if not hdr:
            raise RuntimeError('Ria calculator did not load')
        for c, ccy in CORR.items():
            for pm in ('BankAccount', 'PayNearMe'):
                body = {'selections': {'countryFrom': 'US', 'countryTo': c, 'currencyFrom': 'USD', 'currencyTo': ccy, 'amountFrom': AMT,
                                       'paymentMethod': pm, 'deliveryMethod': 'BankDeposit', 'promoId': 0,
                                       'shouldCalcAmountFrom': False, 'shouldCalcVariableRates': False}}
                r = pg.evaluate("""async ([h, b]) => { const r = await fetch('https://public.riamoneytransfer.com/MoneyTransferCalculator/Calculate',
                                  {method: 'POST', headers: h, body: JSON.stringify(b)}); return r.ok ? await r.json() : null }""", [hdr, body])
                k = r and r.get('model') and r['model']['transferDetails']['calculations']
                if k:
                    out[(c, pm)] = (k['exchangeRate'], k['transferFee'], k['taxAmount'])
        b.close()
    return out

def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    rows = []
    import glob, sys
    ria = {}
    manual = sorted(glob.glob(os.path.join(HERE, '..', 'data', 'ria_browser_*.csv')))
    if '--ria-from-file' in sys.argv and manual:
        # Ria's site blocks headless cloud browsers, so on some runs I read its calculator in my own browser
        # and save it as data/ria_browser_<date>.csv; this uses the newest one
        for r in csv.DictReader(open(manual[-1])):
            ria[(r['corridor'], r['payment_method'])] = (float(r['exchange_rate']), float(r['transfer_fee_usd']), float(r['tax_usd']))
        print('Ria quotes from', os.path.basename(manual[-1]))
    else:
        try:
            ria = ria_quotes()
        except Exception as e:
            print('Ria failed:', e)
    for c, ccy in CORR.items():
        try:
            d = wise(ccy)
        except Exception as e:
            print(c, 'Wise feed failed:', e); continue
        mid = None; q = {}
        for p in d['providers']:
            for x in p['quotes']:
                if x.get('targetCountry') not in (None, c):
                    continue
                if x['isConsideredMidMarketRate']:
                    mid = x['rate']
                if p['alias'] in OTHERS:
                    old = q.get(p['alias'])
                    if old is None or x['dateCollected'][:16] > old[3]:
                        q[p['alias']] = (x['rate'], x['fee'], 0.0, x['dateCollected'][:16])
        if not mid:
            continue
        for (cc, pm), (rate, fee, tax) in ria.items():
            if cc == c:
                q['ria-' + ('bank' if pm == 'BankAccount' else 'cash')] = (rate, fee, tax, now[:10])
        for prov, (rate, fee, tax, collected) in q.items():
            cost = fee + tax + AMT * (1 - rate / mid)
            if cost < 0:
                continue   # a rate above mid-market is a promo or a stale quote; I leave it out
            rows.append([now, c, prov, AMT, rate, mid, fee, tax, round(cost, 2), collected])
    new = not os.path.exists(OUT)
    with open(OUT, 'a', newline='') as f:
        w = csv.writer(f)
        if new:
            w.writerow(['run_utc', 'corridor', 'provider', 'send_usd', 'rate', 'mid_rate', 'fee_usd', 'tax_usd', 'all_in_cost_usd', 'quote_date'])
        w.writerows(rows)
    print(f"{len(rows)} quotes appended to data/price_index.csv")
    for c in CORR:
        line = [f"{r[2]} ${r[8]:.2f}" for r in rows if r[1] == c]
        if line: print(c, ' | '.join(line))

if __name__ == '__main__':
    main()

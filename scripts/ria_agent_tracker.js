// Ria US agent tracker. Ria's site blocks cloud browsers, so this runs in the browser console on
// https://www.riamoneytransfer.com/en-us/locations/ (any normal Chrome window). It queries Ria's own
// public locator on a fixed 5x5 grid (~3 miles apart) around ten metro centres, keeps send locations
// within 10 miles of the centre, de-duplicates by locationId and prints a CSV line per metro.
// The locator returns at most ~50 nearest locations per query, so this is a fixed-method SAMPLE, not a
// census. Compare it month to month with the same grid; don't read the level as the true agent count.
(async () => {
  const Q = '?', metros = {Houston:[29.760496,-95.363433],Dallas:[32.776665,-96.796989],LosAngeles:[34.052235,-118.243683],
    Chicago:[41.878113,-87.629799],NewYork_Queens:[40.728224,-73.794852],Miami:[25.761681,-80.191788],Phoenix:[33.448376,-112.074036],
    SanAntonio:[29.424122,-98.493629],Atlanta:[33.748997,-84.387985],Fresno:[36.737797,-119.787125]};
  const step = 0.045, out = ['run_utc,metro,send_locations_within_10mi,queries,queries_at_cap'];
  const now = new Date().toISOString().slice(0, 16) + 'Z';
  for (const [m, [la, lo]] of Object.entries(metros)) {
    const ids = new Set(); let calls = 0, capped = 0;
    for (let i = -2; i <= 2; i++) for (let j = -2; j <= 2; j++) {
      const a = (la + i * step).toFixed(5), b = (lo + j * step / Math.cos(la * Math.PI / 180)).toFixed(5);
      const r = await fetch(`/api/locations/${Q}lat=${a}&lon=${b}&countryTo=US&type=RMT`).then(x => x.json());
      calls++; if (r.length >= 50) capped++;
      for (const x of r) {
        const d = Math.hypot((x.latitude - la) * 69, (x.longitude - lo) * 69 * Math.cos(la * Math.PI / 180));
        if (d <= 10 && x.sendLocation) ids.add(x.locationId);
      }
      await new Promise(z => setTimeout(z, 300));
    }
    out.push([now, m, ids.size, calls, capped].join(','));
  }
  console.log(out.join('\n'));
})();

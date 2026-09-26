# TraceMapper API examples

Working examples for the [TraceMapper](https://tracemapper.com) REST API in **curl**, **Python** and **JavaScript**.

TraceMapper is a visual traceroute: it maps the path between a measurement point and any host, hop by hop, with latency, packet loss, jitter, geolocation and the network (ASN) behind every router. The API gives you the same data as JSON, plus ping, DNS, HTTP/TLS, port, WHOIS, BGP, IP reputation, email (SPF, DKIM, DMARC) and subdomain lookups.

Full reference: **[tracemapper.com/docs](https://tracemapper.com/docs)**

## Get a key

API access comes with the [Pro and Business plans](https://tracemapper.com/pricing). Generate a key from your account page, then:

```bash
export TRACEMAPPER_API_KEY=tm_...
```

The key goes in the `Authorization` header, never in the query string:

```bash
curl -H "Authorization: Bearer $TRACEMAPPER_API_KEY" \
  "https://tracemapper.com/api/v1/trace?dest=1.1.1.1"
```

## Examples

| Folder | What it shows |
|---|---|
| [`curl/examples.sh`](curl/examples.sh) | One call to every endpoint |
| [`python/trace.py`](python/trace.py) | Print a traceroute hop by hop, with ASN and location |
| [`python/check_route.py`](python/check_route.py) | Exit non-zero when a route is slow or losing packets (for cron or CI) |
| [`javascript/compare-sources.mjs`](javascript/compare-sources.mjs) | Trace one host from several countries and compare latency and networks |

The clients (`python/tracemapper.py`, `javascript/tracemapper.mjs`) have no dependencies: Python 3.9+ standard library, Node 18+ built-in `fetch`.

```bash
cd python && python trace.py example.com
cd javascript && node compare-sources.mjs example.com local paris gp-us-east
```

## Endpoints

| Endpoint | Parameters |
|---|---|
| `GET /api/v1/trace` | `dest`, `source` (default `local`), `protocol` (`icmp`, `udp`, `tcp`), `maxHops` |
| `GET /api/v1/traces` | `limit`, `offset`, `dest`: your saved traces |
| `GET /api/v1/ping` | `host`, `count`, `family` |
| `GET /api/v1/dns` | `domain`, `type`, `resolver` |
| `GET /api/v1/http-check` | `url` |
| `GET /api/v1/port-check` | `host`, and `port` (one port) or `ports=common` (21 common ports), `timeout` |
| `GET /api/v1/whois` | `ip` |
| `GET /api/v1/bgp` | `target`: an IP, a prefix or an ASN (`AS15169`) |
| `GET /api/v1/ip-reputation` | `ip` |
| `GET /api/v1/email-check` | `domain`, `selectors` |
| `GET /api/v1/subdomains` | `domain` |
| `GET /api/v1/outages` | `asn`, `range` |
| `GET /api/v1/status` | none, no key needed: service status and the list of `source` ids |

A real response from `source=gp-us-east` (New York), last hop shown:

```json
{
  "dest": "1.1.1.1",
  "source": "gp-us-east",
  "protocol": "icmp",
  "totalHops": 13,
  "hops": [
    {
      "hopNumber": 13,
      "ip": "1.1.1.1",
      "hostname": "one.one.one.one",
      "asn": 13335,
      "asnOrg": "Cloudflare, Inc.",
      "city": null,
      "countryCode": null,
      "latencyAvg": 14.7,
      "packetLoss": 0,
      "jitter": 0.1,
      "isTimeout": false
    }
  ]
}
```

## Measurement sources

`source=local` traces from Falkenstein, Germany. Other ids trace from Gravelines (France) and from probes on every continent; `GET /api/v1/status` lists them all. Use them to tell a problem on your side of the path from one near the destination.

## Limits and errors

- 60 requests per minute per key on Pro, 300 on Business. A `429` carries a `Retry-After` header.
- One trace at a time per account: a second concurrent trace returns `429 TOO_MANY_CONCURRENT`.
- Errors are JSON with a stable `error` code, for example `API_KEY_MISSING`, `API_KEY_INVALID`, `INVALID_DESTINATION`, `BLOCKED_TARGET` (private or reserved addresses), `UNKNOWN_SOURCE`, `SOURCE_UNAVAILABLE`.

## Reading a trace

Judge the path by the **last hop**. Routers answer traceroute probes at low priority, so an intermediate hop can show loss or a latency spike that real traffic never sees. Loss that starts at one hop and continues to the destination is the real signal. More in the [glossary](https://tracemapper.com/glossary) and the [blog](https://tracemapper.com/blog).

## License

The example code in this repository is MIT licensed. The TraceMapper service itself is a commercial product: see the [terms](https://tracemapper.com/terms).

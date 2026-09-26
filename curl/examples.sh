#!/usr/bin/env bash
# TraceMapper API v1 with curl.
# Usage: TRACEMAPPER_API_KEY=tm_... ./examples.sh
set -euo pipefail

BASE="${TRACEMAPPER_BASE_URL:-https://tracemapper.com}/api/v1"
AUTH="Authorization: Bearer ${TRACEMAPPER_API_KEY:?Set TRACEMAPPER_API_KEY (Pro or Business plan)}"

# Service status and the list of measurement sources (no key needed).
curl -s "$BASE/status"; echo

# Traceroute from the default source (Falkenstein, Germany).
curl -s -H "$AUTH" "$BASE/trace?dest=1.1.1.1&protocol=icmp&maxHops=30"; echo

# Same trace from another country. Source ids come from /status.
curl -s -H "$AUTH" "$BASE/trace?dest=example.com&source=gp-us-east"; echo

# Ping, DNS, HTTP/TLS, ports.
curl -s -H "$AUTH" "$BASE/ping?host=1.1.1.1&count=4"; echo
curl -s -H "$AUTH" "$BASE/dns?domain=example.com&type=MX"; echo
curl -s -H "$AUTH" "$BASE/http-check?url=https://example.com"; echo
curl -s -H "$AUTH" "$BASE/port-check?host=example.com&port=443"; echo
curl -s -H "$AUTH" "$BASE/port-check?host=example.com&ports=common"; echo  # 21 common ports

# Who owns an address, and how it is routed.
curl -s -H "$AUTH" "$BASE/whois?ip=8.8.8.8"; echo
curl -s -H "$AUTH" "$BASE/bgp?target=AS15169"; echo
curl -s -H "$AUTH" "$BASE/ip-reputation?ip=8.8.8.8"; echo

# Mail setup, subdomains from Certificate Transparency, Internet outages.
curl -s -H "$AUTH" "$BASE/email-check?domain=example.com"; echo
curl -s -H "$AUTH" "$BASE/subdomains?domain=example.com"; echo
curl -s -H "$AUTH" "$BASE/outages"; echo

# Your saved trace history.
curl -s -H "$AUTH" "$BASE/traces?limit=5"; echo

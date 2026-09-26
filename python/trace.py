"""Print a traceroute hop by hop.

    python trace.py 1.1.1.1
    python trace.py example.com gp-us-east
"""

import sys

from tracemapper import TraceMapper

dest = sys.argv[1] if len(sys.argv) > 1 else "1.1.1.1"
source = sys.argv[2] if len(sys.argv) > 2 else "local"

result = TraceMapper().trace(dest, source=source)
print(f"{result['dest']} from {result['source']} ({result['protocol']}), {result['totalHops']} hops\n")
for hop in result["hops"]:
    if hop["isTimeout"]:
        print(f"{hop['hopNumber']:>3}  *")
        continue
    where = ", ".join(filter(None, [hop["city"], hop["countryCode"]]))
    network = f"AS{hop['asn']} {hop['asnOrg']}" if hop["asn"] else ""
    latency = f"{hop['latencyAvg']:.1f} ms" if hop["latencyAvg"] is not None else "-"
    loss = f"{hop['packetLoss']:.0f}% loss" if hop["packetLoss"] else ""
    print(f"{hop['hopNumber']:>3}  {hop['ip']:<40} {latency:>9}  {loss:<9} {network}  {where}")

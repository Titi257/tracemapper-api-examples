"""Exit non-zero when the destination is slow or losing packets.

Run it from cron or CI and alert on the exit code:

    python check_route.py api.example.com --max-latency 80 --max-loss 5

Judge the LAST hop (the destination). Intermediate routers often rate-limit
the probes that traceroute sends and show loss or high latency that real
traffic never sees.
"""

import argparse
import sys

from tracemapper import TraceMapper

parser = argparse.ArgumentParser()
parser.add_argument("dest")
parser.add_argument("--source", default="local")
parser.add_argument("--max-latency", type=float, default=100.0, help="milliseconds")
parser.add_argument("--max-loss", type=float, default=10.0, help="percent")
args = parser.parse_args()

hops = TraceMapper().trace(args.dest, source=args.source)["hops"]
last = hops[-1] if hops else None
if last is None or last["isTimeout"]:
    print(f"FAIL {args.dest}: destination did not answer")
    sys.exit(2)

latency, loss = last["latencyAvg"] or 0.0, last["packetLoss"] or 0.0
status = "OK" if latency <= args.max_latency and loss <= args.max_loss else "FAIL"
print(f"{status} {args.dest}: {latency:.1f} ms, {loss:.0f}% loss over {len(hops)} hops")
sys.exit(0 if status == "OK" else 1)

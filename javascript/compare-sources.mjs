// Trace the same destination from several countries and compare the result.
//
//   node compare-sources.mjs example.com local paris gp-us-east
//
// Source ids come from GET /api/v1/status. Sources other than the default
// need a Pro or Business plan.

import { TraceMapper } from "./tracemapper.mjs";

const [dest = "1.1.1.1", ...sources] = process.argv.slice(2);
const client = new TraceMapper();

// One trace at a time per account: a second concurrent trace is refused with
// 429 TOO_MANY_CONCURRENT, so run them one after the other.
for (const source of sources.length ? sources : ["local", "paris"]) {
  let result;
  try {
    result = await client.trace(dest, { source });
  } catch (error) {
    console.log(`${source.padEnd(12)} error: ${error.message}`);
    continue;
  }
  const { hops } = result;
  const last = hops.at(-1);
  const answered = last && !last.isTimeout;
  const latency = answered ? `${last.latencyAvg?.toFixed(1)} ms` : "no answer";
  const networks = [...new Set(hops.filter((h) => h.asn).map((h) => `AS${h.asn}`))].join(" > ");
  console.log(`${source.padEnd(12)} ${String(hops.length).padStart(2)} hops  ${latency.padStart(9)}  ${networks}`);
}

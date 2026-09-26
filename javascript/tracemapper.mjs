// Minimal TraceMapper API v1 client. No dependencies (Node 18+).

export class TraceMapperError extends Error {
  constructor(status, code, message) {
    super([status, code, message].filter(Boolean).join(" "));
    this.status = status;
    this.code = code;
  }
}

export class TraceMapper {
  constructor({ apiKey = process.env.TRACEMAPPER_API_KEY, baseUrl = process.env.TRACEMAPPER_BASE_URL } = {}) {
    if (!apiKey) throw new Error("Set TRACEMAPPER_API_KEY or pass apiKey (Pro or Business plan).");
    this.apiKey = apiKey;
    this.baseUrl = (baseUrl ?? "https://tracemapper.com").replace(/\/$/, "");
  }

  async get(path, params = {}) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, value]) => value !== undefined).map(([k, v]) => [k, String(v)]),
    );
    const qs = query.toString();
    const url = `${this.baseUrl}/api/v1/${path}${qs ? `?${qs}` : ""}`;
    const response = await fetch(url, { headers: { Authorization: `Bearer ${this.apiKey}` } });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new TraceMapperError(response.status, body.error, body.message);
    return body;
  }

  trace(dest, { source = "local", protocol = "icmp", maxHops = 30 } = {}) {
    return this.get("trace", { dest, source, protocol, maxHops });
  }

  ping(host, count = 4) {
    return this.get("ping", { host, count });
  }

  dns(domain, type = "A") {
    return this.get("dns", { domain, type });
  }

  whois(ip) {
    return this.get("whois", { ip });
  }

  bgp(target) {
    return this.get("bgp", { target });
  }
}

import { useEffect, useState } from "react";

type ServiceStatus = "online" | "checking";

interface Service {
  name: string;
  nameAr: string;
  detail: string;
  status: ServiceStatus;
  icon: string;
}

const SERVICES: Service[] = [
  { name: "OpenClaw Gateway", nameAr: "OpenClaw Gateway", detail: "@Clawdo_My_bot", status: "online", icon: "🤖" },
  { name: "LiteLLM Proxy", nameAr: "LiteLLM Proxy", detail: "10 مفاتيح · round-robin", status: "online", icon: "⚡" },
  { name: "Telegram Channel", nameAr: "تيليغرام", detail: "خاص · DM فقط", status: "online", icon: "✈️" },
];

function useUptime() {
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, []);
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function App() {
  const uptime = useUptime();
  const [pulse, setPulse] = useState(true);
  useEffect(() => {
    const t = setInterval(() => setPulse((p) => !p), 1200);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0f1117 0%, #1a1f35 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif",
      padding: "24px",
      direction: "rtl",
    }}>
      <div style={{ maxWidth: 480, width: "100%" }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 36 }}>
          <div style={{ fontSize: 72, marginBottom: 12, lineHeight: 1 }}>🤖</div>
          <h1 style={{ color: "#f0f4ff", fontSize: 30, fontWeight: 700, margin: 0 }}>Clawdo Bot</h1>
          <p style={{ color: "#64748b", fontSize: 15, marginTop: 6 }}>
            مساعد شخصي · 24/7 · Gemini 3.5 Flash
          </p>

          {/* Live badge */}
          <div style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            background: "#0d2218",
            border: "1px solid #166534",
            borderRadius: 999,
            padding: "6px 16px",
            marginTop: 14,
          }}>
            <span style={{
              width: 8, height: 8,
              background: "#4ade80",
              borderRadius: "50%",
              display: "inline-block",
              boxShadow: pulse ? "0 0 0 4px rgba(74,222,128,0.2)" : "none",
              transition: "box-shadow 0.4s ease",
            }} />
            <span style={{ color: "#4ade80", fontSize: 13, fontWeight: 600 }}>يعمل الآن</span>
            <span style={{ color: "#166534", fontSize: 13 }}>· {uptime}</span>
          </div>
        </div>

        {/* Services */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 24 }}>
          {SERVICES.map((svc) => (
            <div key={svc.name} style={{
              background: "rgba(255,255,255,0.04)",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: 14,
              padding: "16px 20px",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <span style={{ fontSize: 22 }}>{svc.icon}</span>
                <div>
                  <div style={{ color: "#e2e8f0", fontSize: 14, fontWeight: 600 }}>{svc.nameAr}</div>
                  <div style={{ color: "#475569", fontSize: 12, marginTop: 2 }}>{svc.detail}</div>
                </div>
              </div>
              <div style={{
                display: "flex", alignItems: "center", gap: 6,
                background: "#0d2218", border: "1px solid #166534",
                borderRadius: 999, padding: "4px 12px",
              }}>
                <span style={{ width: 6, height: 6, background: "#4ade80", borderRadius: "50%", display: "inline-block" }} />
                <span style={{ color: "#4ade80", fontSize: 12, fontWeight: 600 }}>متصل</span>
              </div>
            </div>
          ))}
        </div>

        {/* Model & Keys */}
        <div style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.06)",
          borderRadius: 14,
          padding: "16px 20px",
          marginBottom: 20,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: 12,
        }}>
          <div>
            <div style={{ color: "#64748b", fontSize: 12, marginBottom: 4 }}>النموذج</div>
            <code style={{
              background: "#1e2b45", color: "#93c5fd",
              padding: "4px 10px", borderRadius: 6, fontSize: 13,
            }}>gemini-2.5-flash</code>
          </div>
          <div style={{ textAlign: "left" }}>
            <div style={{ color: "#64748b", fontSize: 12, marginBottom: 4 }}>مفاتيح API</div>
            <div style={{ color: "#e2e8f0", fontSize: 14, fontWeight: 600 }}>
              10 مفاتيح <span style={{ color: "#64748b", fontSize: 12 }}>· Google AI Studio</span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{ textAlign: "center", color: "#334155", fontSize: 12 }}>
          <a href="/api/healthz" style={{ color: "#334155", textDecoration: "none" }}>healthz</a>
          {" · "}
          <a href="/api/status" style={{ color: "#334155", textDecoration: "none" }}>api status</a>
        </div>

      </div>
    </div>
  );
}

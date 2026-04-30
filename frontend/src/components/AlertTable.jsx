import { useAlerts } from "../hooks/useAlerts";

const ATTACK_COLORS = {
  port_scan: { bg: "#451a03", text: "#fbbf24", label: "Port Scan" },
  brute_force: { bg: "#450a0a", text: "#f87171", label: "Brute Force" },
  dos_attack: { bg: "#2e1065", text: "#c084fc", label: "DoS" },
  ml_anomaly: { bg: "#082f49", text: "#38bdf8", label: "ML Anomaly" },
};

export default function AlertTable() {
  const { alerts, loading } = useAlerts();

  return (
    <div
      style={{
        background: "#1e293b",
        border: "1px solid #334155",
        borderRadius: "10px",
        padding: "20px",
      }}
    >
      <h3
        style={{
          color: "#f1f5f9",
          margin: "0 0 16px",
          fontSize: "14px",
          fontWeight: 600,
        }}
      >
        Live Alert Feed
        <span
          style={{
            marginLeft: "8px",
            background: "#ef4444",
            color: "#fff",
            borderRadius: "999px",
            padding: "1px 8px",
            fontSize: "11px",
          }}
        >
          LIVE
        </span>
      </h3>
      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "13px",
          }}
        >
          <thead>
            <tr>
              {[
                "Time",
                "Source IP",
                "Attack Type",
                "Confidence",
                "Details",
              ].map((h) => (
                <th
                  key={h}
                  style={{
                    color: "#64748b",
                    textAlign: "left",
                    padding: "8px 12px",
                    borderBottom: "1px solid #334155",
                    whiteSpace: "nowrap",
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td
                  colSpan={5}
                  style={{
                    color: "#64748b",
                    textAlign: "center",
                    padding: "32px",
                  }}
                >
                  Loading...
                </td>
              </tr>
            ) : alerts.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  style={{
                    color: "#64748b",
                    textAlign: "center",
                    padding: "32px",
                  }}
                >
                  No alerts yet — run a simulation
                </td>
              </tr>
            ) : (
              alerts.map((alert) => {
                const style = ATTACK_COLORS[alert.attack_type] || {
                  bg: "#1e293b",
                  text: "#94a3b8",
                  label: alert.attack_type,
                };
                return (
                  <tr
                    key={alert.id}
                    style={{ borderBottom: "1px solid #1e293b" }}
                  >
                    <td
                      style={{
                        padding: "10px 12px",
                        color: "#64748b",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </td>
                    <td
                      style={{
                        padding: "10px 12px",
                        color: "#e2e8f0",
                        fontFamily: "monospace",
                      }}
                    >
                      {alert.src_ip}
                    </td>
                    <td style={{ padding: "10px 12px" }}>
                      <span
                        style={{
                          background: style.bg,
                          color: style.text,
                          padding: "2px 10px",
                          borderRadius: "999px",
                          fontSize: "11px",
                          fontWeight: 600,
                        }}
                      >
                        {style.label}
                      </span>
                    </td>
                    <td style={{ padding: "10px 12px", color: "#94a3b8" }}>
                      {(alert.confidence * 100).toFixed(0)}%
                    </td>
                    <td
                      style={{
                        padding: "10px 12px",
                        color: "#64748b",
                        maxWidth: "240px",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {alert.details}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

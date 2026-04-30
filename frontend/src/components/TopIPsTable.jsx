import { useEffect, useState } from "react";
import client from "../api/client";

export default function TopIPsTable() {
  const [ips, setIps] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await client.get("/api/ips/top?limit=8");
        setIps(res.data);
      } catch (e) {}
    };
    fetch();
    const id = setInterval(fetch, 4000);
    return () => clearInterval(id);
  }, []);

  const max = ips[0]?.count || 1;

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
        Top Source IPs
      </h3>
      {ips.map((entry, i) => (
        <div key={entry.ip} style={{ marginBottom: "10px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "4px",
            }}
          >
            <span
              style={{
                color: "#e2e8f0",
                fontFamily: "monospace",
                fontSize: "13px",
              }}
            >
              {entry.ip}
            </span>
            <span style={{ color: "#64748b", fontSize: "12px" }}>
              {entry.count.toLocaleString()} pkts
            </span>
          </div>
          <div
            style={{
              background: "#0f172a",
              borderRadius: "4px",
              height: "4px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${(entry.count / max) * 100}%`,
                background: i === 0 ? "#ef4444" : "#3b82f6",
                borderRadius: "4px",
                transition: "width 0.4s ease",
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

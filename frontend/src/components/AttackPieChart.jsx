import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import client from "../api/client";

const COLORS = {
  port_scan: "#f59e0b",
  brute_force: "#ef4444",
  dos_attack: "#8b5cf6",
  ml_anomaly: "#06b6d4",
};

export default function AttackPieChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await client.get("/api/alerts/types");
        setData(
          res.data.map((d) => ({
            name: d.type.replace("_", " "),
            value: d.count,
            key: d.type,
          })),
        );
      } catch (e) {}
    };
    fetch();
    const id = setInterval(fetch, 5000);
    return () => clearInterval(id);
  }, []);

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
        Attack Type Breakdown
      </h3>
      {data.length === 0 ? (
        <p style={{ color: "#64748b", textAlign: "center", padding: "40px 0" }}>
          No attacks detected yet
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              outerRadius={70}
              dataKey="value"
              label
            >
              {data.map((entry, i) => (
                <Cell key={i} fill={COLORS[entry.key] || "#94a3b8"} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                background: "#0f172a",
                border: "1px solid #334155",
                color: "#f1f5f9",
              }}
            />
            <Legend wrapperStyle={{ color: "#94a3b8", fontSize: "12px" }} />
          </PieChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

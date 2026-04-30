import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useTraffic } from "../hooks/useTraffic";

export default function TrafficChart() {
  const traffic = useTraffic();

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
        Live Traffic — Packets / Sec
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={traffic}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 11 }} />
          <YAxis tick={{ fill: "#64748b", fontSize: 11 }} />
          <Tooltip
            contentStyle={{
              background: "#0f172a",
              border: "1px solid #334155",
              color: "#f1f5f9",
            }}
          />
          <Line
            type="monotone"
            dataKey="pps"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

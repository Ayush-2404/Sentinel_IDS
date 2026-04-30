import { useStats } from "../hooks/useStats";
import StatCard from "../components/StatCard";
import TrafficChart from "../components/TrafficChart";
import AttackPieChart from "../components/AttackPieChart";
import AlertTable from "../components/AlertTable";
import TopIPsTable from "../components/TopIPsTable";

export default function Dashboard() {
  const { stats } = useStats();

  return (
    <div style={{ padding: "24px", maxWidth: "1400px", margin: "0 auto" }}>
      {/* Summary Cards */}
      <div
        style={{
          display: "flex",
          gap: "16px",
          flexWrap: "wrap",
          marginBottom: "20px",
        }}
      >
        <StatCard
          title="Total Packets"
          value={stats.total_packets}
          color="#3b82f6"
          subtitle="Captured since start"
        />
        <StatCard
          title="Total Alerts"
          value={stats.total_alerts}
          color="#ef4444"
          subtitle="All attack types"
        />
        <StatCard
          title="Blocked IPs"
          value={stats.blocked_ips}
          color="#f59e0b"
          subtitle="Auto + manual"
        />
      </div>

      {/* Charts Row */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: "16px",
          marginBottom: "20px",
        }}
      >
        <TrafficChart />
        <AttackPieChart />
      </div>

      {/* Bottom Row */}
      <div
        style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "16px" }}
      >
        <TopIPsTable />
        <AlertTable />
      </div>
    </div>
  );
}

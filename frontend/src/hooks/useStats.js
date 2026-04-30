import { useState, useEffect } from "react";
import client from "../api/client";

export function useStats(intervalMs = 3000) {
  const [stats, setStats] = useState({
    total_packets: 0,
    total_alerts: 0,
    blocked_ips: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await client.get("/api/stats/summary");
        setStats(res.data);
        setLoading(false);
      } catch (e) {
        console.error("Stats fetch failed:", e);
      }
    };

    fetch();
    const interval = setInterval(fetch, intervalMs);
    return () => clearInterval(interval);
  }, [intervalMs]);

  return { stats, loading };
}

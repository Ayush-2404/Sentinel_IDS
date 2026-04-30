import { useState, useEffect } from "react";
import client from "../api/client";

export function useAlerts(intervalMs = 2000) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await client.get("/api/alerts/?limit=50");
        setAlerts(res.data);
        setLoading(false);
      } catch (e) {
        console.error("Alerts fetch failed:", e);
      }
    };

    fetch();
    const interval = setInterval(fetch, intervalMs);
    return () => clearInterval(interval);
  }, [intervalMs]);

  return { alerts, loading };
}

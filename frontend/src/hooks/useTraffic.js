import { useState, useEffect } from "react";
import client from "../api/client";

export function useTraffic(intervalMs = 3000) {
  const [traffic, setTraffic] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await client.get("/api/stats/traffic?limit=30");
        setTraffic(res.data);
      } catch (e) {
        console.error("Traffic fetch failed:", e);
      }
    };

    fetch();
    const interval = setInterval(fetch, intervalMs);
    return () => clearInterval(interval);
  }, [intervalMs]);

  return traffic;
}

export default function NavBar() {
  return (
    <nav
      style={{
        background: "#0f172a",
        borderBottom: "1px solid #1e293b",
        padding: "0 24px",
        height: "56px",
        display: "flex",
        alignItems: "center",
        gap: "12px",
      }}
    >
      <span style={{ color: "#ef4444", fontSize: "18px" }}>◉</span>
      <span
        style={{
          color: "#f1f5f9",
          fontWeight: 700,
          fontSize: "15px",
          letterSpacing: "0.02em",
        }}
      >
        Hybrid IDS
      </span>
      <span style={{ color: "#334155", margin: "0 4px" }}>|</span>
      <span style={{ color: "#64748b", fontSize: "13px" }}>
        Real-time Intrusion Detection
      </span>
      <div
        style={{
          marginLeft: "auto",
          display: "flex",
          alignItems: "center",
          gap: "6px",
        }}
      >
        <span
          style={{
            width: "8px",
            height: "8px",
            borderRadius: "50%",
            background: "#22c55e",
            display: "inline-block",
          }}
        />
        <span style={{ color: "#22c55e", fontSize: "12px" }}>
          System Active
        </span>
      </div>
    </nav>
  );
}

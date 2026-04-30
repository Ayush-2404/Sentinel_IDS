export default function StatCard({
  title,
  value,
  subtitle,
  color = "#3b82f6",
}) {
  return (
    <div
      style={{
        background: "#1e293b",
        border: `1px solid #334155`,
        borderTop: `3px solid ${color}`,
        borderRadius: "10px",
        padding: "20px 24px",
        flex: 1,
        minWidth: "180px",
      }}
    >
      <p
        style={{
          color: "#94a3b8",
          fontSize: "12px",
          margin: "0 0 8px",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
        }}
      >
        {title}
      </p>
      <p
        style={{
          color: "#f1f5f9",
          fontSize: "32px",
          fontWeight: 700,
          margin: "0 0 4px",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        {value?.toLocaleString() ?? "—"}
      </p>
      {subtitle && (
        <p style={{ color: "#64748b", fontSize: "12px", margin: 0 }}>
          {subtitle}
        </p>
      )}
    </div>
  );
}

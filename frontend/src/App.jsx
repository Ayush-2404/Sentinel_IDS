import NavBar from "./components/NavBar";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <div
      style={{
        background: "#0f172a",
        minHeight: "100vh",
        fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      }}
    >
      <NavBar />
      <Dashboard />
    </div>
  );
}

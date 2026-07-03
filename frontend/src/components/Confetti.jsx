const COLORS = ["#fb923c", "#f43f5e", "#facc15", "#34d399", "#60a5fa"];

export default function Confetti({ pieces = 40 }) {
  const items = Array.from({ length: pieces }, (_, i) => {
    const left = Math.random() * 100;
    const delay = Math.random() * 0.4;
    const duration = 2.2 + Math.random() * 1.2;
    const color = COLORS[i % COLORS.length];
    const rotate = Math.random() > 0.5 ? "0" : "50%";

    return (
      <span
        key={i}
        className="confetti-piece"
        style={{
          left: `${left}%`,
          backgroundColor: color,
          animationDelay: `${delay}s`,
          animationDuration: `${duration}s`,
          borderRadius: rotate,
        }}
      />
    );
  });

  return <div aria-hidden="true">{items}</div>;
}

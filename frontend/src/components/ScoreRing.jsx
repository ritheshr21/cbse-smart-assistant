export default function ScoreRing({ value, max, size = 96, label }) {
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const pct = max > 0 ? Math.max(0, Math.min(1, value / max)) : 0;
  const offset = circumference * (1 - pct);

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <defs>
          <linearGradient id="ring-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fb923c" />
            <stop offset="100%" stopColor="#f43f5e" />
          </linearGradient>
        </defs>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#f1f5f9" strokeWidth="8" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="url(#ring-gradient)"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.8s ease-out" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display font-bold text-slate-800" style={{ fontSize: size * 0.24 }}>
          {value}/{max}
        </span>
        {label && <span className="text-[10px] text-slate-400 font-medium">{label}</span>}
      </div>
    </div>
  );
}

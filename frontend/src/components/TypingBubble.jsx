export default function TypingBubble() {
  return (
    <div className="flex items-center gap-1.5 bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3.5 shadow-sm w-fit">
      <span className="typing-dot w-2 h-2 rounded-full bg-orange-400" />
      <span className="typing-dot w-2 h-2 rounded-full bg-orange-400" />
      <span className="typing-dot w-2 h-2 rounded-full bg-orange-400" />
    </div>
  );
}

import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import SourceCard from "./SourceCard";
import TypingBubble from "./TypingBubble";
import { SendIcon, ChatIcon } from "./icons";

export default function ChatView({ messages, setMessages }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  const ask = async () => {
    const question = input.trim();
    if (!question || loading) return;

    setInput("");
    setError(null);
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    try {
      const data = await api.chat(question);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer, sources: data.sources || [] },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      ask();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-8 py-6 space-y-5">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 gap-3">
            <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
              <ChatIcon className="w-7 h-7 text-orange-400" />
            </div>
            <p className="font-display font-semibold text-slate-500">Ask anything from your NCERT chapters</p>
            <p className="text-sm max-w-sm">
              Try "What is Coulomb's Law?" or "Explain electric field lines" to get a grounded, sourced answer.
            </p>
          </div>
        )}

        {messages.map((m, i) =>
          m.role === "user" ? (
            <div key={i} className="animate-in flex justify-end">
              <div className="max-w-[75%] bg-gradient-to-br from-orange-500 to-rose-500 text-white rounded-2xl rounded-br-sm px-4 py-3 shadow-sm shadow-orange-200">
                <p className="text-sm leading-relaxed">{m.text}</p>
              </div>
            </div>
          ) : (
            <div key={i} className="animate-in flex flex-col gap-3">
              <div className="max-w-[85%] bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3.5 shadow-sm">
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">{m.text}</p>
              </div>
              {m.sources?.length > 0 && (
                <div className="flex gap-3 overflow-x-auto pb-1 pl-1">
                  {m.sources.map((s, j) => (
                    <SourceCard key={j} source={s} />
                  ))}
                </div>
              )}
            </div>
          )
        )}

        {loading && (
          <div className="animate-in">
            <TypingBubble />
          </div>
        )}

        {error && (
          <div className="text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-4 py-3">
            {error}
          </div>
        )}
      </div>

      <div className="px-8 pb-6 pt-2">
        <div className="flex items-end gap-2 bg-white border border-slate-200 rounded-2xl shadow-sm px-3 py-2 focus-within:border-orange-300 focus-within:ring-4 focus-within:ring-orange-50 transition-all">
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your NCERT chapters..."
            className="flex-1 resize-none bg-transparent outline-none text-sm text-slate-700 placeholder:text-slate-400 py-2 px-2 max-h-32"
          />
          <button
            onClick={ask}
            disabled={loading || !input.trim()}
            className="shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 text-white flex items-center justify-center shadow-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-md transition-all cursor-pointer"
          >
            <SendIcon className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

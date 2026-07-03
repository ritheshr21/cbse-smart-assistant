import { useState } from "react";
import { api } from "../api";
import { parseEvaluation } from "../utils/parseEvaluation";
import { BrainIcon, LightbulbIcon } from "./icons";

function RubricBar({ label, value, max }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  const color = pct === 100 ? "from-emerald-400 to-emerald-500" : pct > 0 ? "from-amber-400 to-amber-500" : "from-rose-400 to-rose-500";

  return (
    <div>
      <div className="flex justify-between text-xs font-medium text-slate-500 mb-1">
        <span>{label}</span>
        <span>
          {value}/{max}
        </span>
      </div>
      <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${color} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export default function EvaluateView() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const evaluate = async () => {
    if (!question.trim() || !answer.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.evaluate(question.trim(), answer.trim());
      setResult({ ...data, parsed: parseEvaluation(data.evaluation) });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full overflow-y-auto px-8 py-6">
      <div className="max-w-2xl mx-auto space-y-4">
        <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm space-y-3">
          <div>
            <label className="text-xs font-semibold text-slate-500 mb-1 block">Question</label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows={2}
              placeholder="Paste or type the question..."
              className="w-full resize-none bg-slate-50 rounded-xl outline-none text-sm text-slate-700 placeholder:text-slate-400 px-3.5 py-2.5 border border-transparent focus:border-orange-300 focus:bg-white transition-colors"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-500 mb-1 block">Your Answer</label>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={5}
              placeholder="Write your answer here..."
              className="w-full resize-none bg-slate-50 rounded-xl outline-none text-sm text-slate-700 placeholder:text-slate-400 px-3.5 py-2.5 border border-transparent focus:border-orange-300 focus:bg-white transition-colors"
            />
          </div>
          <button
            onClick={evaluate}
            disabled={loading || !question.trim() || !answer.trim()}
            className="w-full py-3 rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 text-white text-sm font-semibold shadow-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-md transition-all cursor-pointer"
          >
            {loading ? "Evaluating..." : "Evaluate Answer"}
          </button>
        </div>

        {error && (
          <div className="text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        {!result && !loading && !error && (
          <div className="flex flex-col items-center text-center text-slate-400 gap-3 mt-10">
            <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
              <BrainIcon className="w-7 h-7 text-orange-400" />
            </div>
            <p className="font-display font-semibold text-slate-500">Get examiner-style feedback</p>
            <p className="text-sm max-w-sm">Your answer is scored against the CBSE marking scheme.</p>
          </div>
        )}

        {result && (
          <div className="animate-in space-y-4">
            <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm space-y-4">
              {result.parsed.total !== null ? (
                <>
                  <div className="flex items-center justify-between">
                    <p className="font-display font-bold text-slate-800">Marking Breakdown</p>
                    <span className="font-display font-bold text-xl bg-gradient-to-r from-orange-500 to-rose-500 bg-clip-text text-transparent">
                      {result.parsed.total}/5
                    </span>
                  </div>
                  <RubricBar label="Content Accuracy" value={result.parsed.contentAccuracy ?? 0} max={2} />
                  <RubricBar label="Explanation" value={result.parsed.explanation ?? 0} max={2} />
                  <RubricBar label="Clarity" value={result.parsed.clarity ?? 0} max={1} />
                </>
              ) : (
                <pre className="text-sm text-slate-600 whitespace-pre-wrap font-sans">{result.evaluation}</pre>
              )}

              {result.parsed.feedback && (
                <div className="bg-orange-50 border border-orange-100 rounded-xl px-4 py-3">
                  <p className="text-xs font-semibold text-orange-600 mb-1">Feedback</p>
                  <p className="text-sm text-slate-600 leading-relaxed">{result.parsed.feedback}</p>
                </div>
              )}

              {result.parsed.weakAreas.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-slate-500 mb-1.5">Weak Areas</p>
                  <ul className="space-y-1">
                    {result.parsed.weakAreas.map((point, i) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                        <span className="w-1 h-1 rounded-full bg-rose-400 mt-2 shrink-0" />
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm">
                <p className="text-xs font-semibold text-slate-500 mb-2.5">Weak Topics (overall)</p>
                {result.weak_topics?.length > 0 ? (
                  <div className="flex flex-wrap gap-1.5">
                    {result.weak_topics.map((wt, i) => (
                      <span
                        key={i}
                        className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-rose-50 text-rose-600 border border-rose-100"
                      >
                        {wt.topic} · {wt.mistakes}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-600 border border-emerald-100">
                    No weak topics yet 🎉
                  </span>
                )}
              </div>

              <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm">
                <p className="text-xs font-semibold text-slate-500 mb-2.5 flex items-center gap-1.5">
                  <LightbulbIcon className="w-3.5 h-3.5 text-amber-400" />
                  Suggestions
                </p>
                {result.suggestions?.length > 0 ? (
                  <ul className="space-y-1">
                    {result.suggestions.map((s, i) => (
                      <li key={i} className="text-sm text-slate-600">
                        {s}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-slate-400">Nothing to suggest yet — keep going!</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

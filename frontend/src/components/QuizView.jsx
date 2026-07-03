import { useState } from "react";
import { api } from "../api";
import ScoreRing from "./ScoreRing";
import Confetti from "./Confetti";
import { QuizIcon, CheckIcon, CrossIcon, SparkleIcon } from "./icons";

export default function QuizView() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mcqs, setMcqs] = useState([]);
  const [rawQuiz, setRawQuiz] = useState("");
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const generate = async () => {
    if (!topic.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setAnswers({});

    try {
      const data = await api.generateQuiz(topic.trim());
      setMcqs(data.mcqs || []);
      setRawQuiz(data.quiz || "");
      if (!data.mcqs?.length) {
        setError("Couldn't parse structured questions from the response. Try a more specific topic.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const answeredCount = Object.values(answers).filter(Boolean).length;
  const allAnswered = mcqs.length > 0 && answeredCount === mcqs.length;

  const submit = async () => {
    if (!allAnswered || submitting) return;
    setSubmitting(true);
    setError(null);

    try {
      const data = await api.submitMcq(answers);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const scoreNum = result ? parseInt(result.score.split("/")[0], 10) : 0;
  const scoreDen = result ? parseInt(result.score.split("/")[1], 10) : 0;
  const celebrate = result && scoreDen > 0 && scoreNum / scoreDen >= 0.7;

  return (
    <div className="h-full overflow-y-auto px-8 py-6">
      {celebrate && <Confetti />}

      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-2xl shadow-sm p-2 mb-2">
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && generate()}
            placeholder="Enter a topic, e.g. Coulomb's Law"
            className="flex-1 bg-transparent outline-none text-sm text-slate-700 placeholder:text-slate-400 px-3 py-2"
          />
          <button
            onClick={generate}
            disabled={loading || !topic.trim()}
            className="shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 text-white text-sm font-semibold shadow-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-md transition-all cursor-pointer"
          >
            <SparkleIcon className="w-4 h-4" />
            {loading ? "Generating..." : "Generate Quiz"}
          </button>
        </div>

        {error && (
          <div className="text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-4 py-3 mb-4">
            {error}
          </div>
        )}

        {!mcqs.length && !loading && !error && (
          <div className="flex flex-col items-center text-center text-slate-400 gap-3 mt-20">
            <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
              <QuizIcon className="w-7 h-7 text-orange-400" />
            </div>
            <p className="font-display font-semibold text-slate-500">Generate a quiz to test yourself</p>
            <p className="text-sm max-w-sm">Pick any topic from your chapters and get instant MCQs.</p>
          </div>
        )}

        {mcqs.length > 0 && (
          <>
            <div className="flex items-center justify-between my-5">
              <p className="text-sm font-semibold text-slate-500">
                {mcqs.length} question{mcqs.length > 1 ? "s" : ""}
              </p>
              {!result && (
                <p className="text-xs font-medium text-slate-400">
                  {answeredCount} / {mcqs.length} answered
                </p>
              )}
            </div>

            <div className="space-y-4">
              {mcqs.map((mcq) => {
                const qid = String(mcq.question_id);
                const detail = result?.details.find((d) => d.question_id === qid);

                return (
                  <div
                    key={qid}
                    className="animate-in bg-white border border-slate-100 rounded-2xl p-5 shadow-sm"
                  >
                    <p className="text-sm font-semibold text-slate-800 mb-3">
                      Q{qid}. {mcq.question}
                    </p>
                    <div className="grid gap-2">
                      {mcq.options.map((opt) => {
                        const selected = answers[qid] === opt.label;
                        const isCorrectOpt = detail && opt.label === detail.correct_answer;
                        const isWrongSelected = detail && selected && !detail.is_correct;

                        let stateClasses = "border-slate-200 hover:border-orange-300 hover:bg-orange-50/50";
                        if (result) {
                          if (isCorrectOpt) stateClasses = "border-emerald-400 bg-emerald-50";
                          else if (isWrongSelected) stateClasses = "border-rose-400 bg-rose-50";
                          else stateClasses = "border-slate-100 opacity-60";
                        } else if (selected) {
                          stateClasses = "border-orange-400 bg-orange-50";
                        }

                        return (
                          <label
                            key={opt.label}
                            className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl border cursor-pointer transition-all ${stateClasses} ${
                              result ? "cursor-default" : ""
                            }`}
                          >
                            <input
                              type="radio"
                              name={`q-${qid}`}
                              className="hidden"
                              disabled={!!result}
                              checked={selected}
                              onChange={() => setAnswers((prev) => ({ ...prev, [qid]: opt.label }))}
                            />
                            <span
                              className={`w-6 h-6 shrink-0 rounded-full flex items-center justify-center text-xs font-bold ${
                                selected || isCorrectOpt
                                  ? "bg-gradient-to-br from-orange-500 to-rose-500 text-white"
                                  : "bg-slate-100 text-slate-500"
                              }`}
                            >
                              {opt.label}
                            </span>
                            <span className="text-sm text-slate-700 flex-1">{opt.text}</span>
                            {result && isCorrectOpt && <CheckIcon className="w-4 h-4 text-emerald-500" />}
                            {result && isWrongSelected && <CrossIcon className="w-4 h-4 text-rose-500" />}
                          </label>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>

            {!result ? (
              <button
                onClick={submit}
                disabled={!allAnswered || submitting}
                className="w-full mt-5 py-3 rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 text-white text-sm font-semibold shadow-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-md transition-all cursor-pointer"
              >
                {submitting ? "Submitting..." : "Submit Answers"}
              </button>
            ) : (
              <div className="mt-6 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex items-center gap-5">
                <ScoreRing value={scoreNum} max={scoreDen} label="SCORE" />
                <div>
                  <p className="font-display font-bold text-slate-800 text-lg">
                    {celebrate ? "Great job! 🎉" : "Keep practicing!"}
                  </p>
                  <p className="text-sm text-slate-500">
                    You got {scoreNum} out of {scoreDen} correct.
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatView from "./components/ChatView";
import QuizView from "./components/QuizView";
import EvaluateView from "./components/EvaluateView";
import { api } from "./api";

const TITLES = {
  chat: { title: "Ask a Question", subtitle: "Get grounded answers with citations from your NCERT chapters." },
  quiz: { title: "Generate a Quiz", subtitle: "Test yourself with instant MCQs on any topic." },
  evaluate: { title: "Evaluate Your Answer", subtitle: "Get examiner-style feedback on the CBSE marking scheme." },
};

function App() {
  const [view, setView] = useState("chat");
  const [messages, setMessages] = useState([]);
  const [online, setOnline] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const check = async () => {
      const ok = await api.health();
      if (!cancelled) setOnline(ok);
    };

    check();
    const interval = setInterval(check, 15000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const { title, subtitle } = TITLES[view];

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#fbf8f4]">
      <Sidebar
        view={view}
        setView={setView}
        online={online}
        showClear={view === "chat" && messages.length > 0}
        onClearChat={() => setMessages([])}
      />

      <main className="flex-1 flex flex-col min-w-0">
        <header className="shrink-0 px-8 pt-7 pb-4">
          <h1 className="font-display font-bold text-2xl text-slate-800">{title}</h1>
          <p className="text-sm text-slate-400 mt-1">{subtitle}</p>
        </header>

        <div className="flex-1 min-h-0">
          {view === "chat" && <ChatView messages={messages} setMessages={setMessages} />}
          {view === "quiz" && <QuizView />}
          {view === "evaluate" && <EvaluateView />}
        </div>
      </main>
    </div>
  );
}

export default App;

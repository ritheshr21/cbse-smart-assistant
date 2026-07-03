import { BookIcon, ChatIcon, QuizIcon, BrainIcon, TrashIcon } from "./icons";

const NAV_ITEMS = [
  { id: "chat", label: "Ask a Question", icon: ChatIcon },
  { id: "quiz", label: "Generate Quiz", icon: QuizIcon },
  { id: "evaluate", label: "Evaluate Answer", icon: BrainIcon },
];

export default function Sidebar({ view, setView, online, onClearChat, showClear }) {
  return (
    <aside className="w-64 shrink-0 h-full bg-white border-r border-slate-100 flex flex-col">
      <div className="px-6 pt-7 pb-6 flex items-center gap-2.5">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-orange-500 to-rose-500 flex items-center justify-center shadow-sm shadow-orange-200">
          <BookIcon className="w-5 h-5 text-white" />
        </div>
        <div>
          <p className="font-display font-bold text-slate-800 leading-tight">CBSE Smart</p>
          <p className="font-display font-bold text-slate-800 leading-tight -mt-0.5">Assistant</p>
        </div>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
          const active = view === id;
          return (
            <button
              key={id}
              onClick={() => setView(id)}
              className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all cursor-pointer ${
                active
                  ? "bg-gradient-to-r from-orange-500 to-rose-500 text-white shadow-md shadow-orange-200"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-700"
              }`}
            >
              <Icon className="w-[18px] h-[18px]" />
              {label}
            </button>
          );
        })}
      </nav>

      <div className="px-4 pb-5 pt-3 space-y-3">
        {showClear && (
          <button
            onClick={onClearChat}
            className="w-full flex items-center justify-center gap-2 px-3.5 py-2 rounded-xl text-sm font-medium text-slate-500 border border-slate-200 hover:bg-slate-50 hover:text-rose-600 hover:border-rose-200 transition-colors cursor-pointer"
          >
            <TrashIcon className="w-4 h-4" />
            Clear chat
          </button>
        )}

        <div className="flex items-center gap-2 px-2 text-xs text-slate-400">
          <span
            className={`w-2 h-2 rounded-full ${online ? "bg-emerald-500" : "bg-slate-300"}`}
          />
          {online === null ? "Checking..." : online ? "Connected" : "Offline"}
        </div>
      </div>
    </aside>
  );
}

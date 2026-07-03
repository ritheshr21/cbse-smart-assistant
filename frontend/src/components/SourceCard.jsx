import { BookIcon, LinkIcon } from "./icons";

export default function SourceCard({ source }) {
  const title = source.chapter_title || source.chapter || "Unknown chapter";
  const subject = source.subject ? String(source.subject).replace(/^\w/, (c) => c.toUpperCase()) : null;
  const klass = source.class;
  const pdfHref = source.pdf_url || source.source_url;

  return (
    <div className="min-w-[240px] max-w-[280px] bg-white border border-slate-100 rounded-2xl p-4 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all">
      <div className="flex items-start gap-2 mb-2">
        <div className="w-7 h-7 shrink-0 rounded-lg bg-orange-50 flex items-center justify-center">
          <BookIcon className="w-3.5 h-3.5 text-orange-500" />
        </div>
        <p className="text-sm font-semibold text-slate-800 leading-snug">{title}</p>
      </div>

      <div className="flex flex-wrap gap-1.5 mb-2">
        {klass && (
          <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
            Class {klass}
          </span>
        )}
        {subject && (
          <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
            {subject}
          </span>
        )}
      </div>

      {source.excerpt && (
        <p className="text-xs text-slate-500 italic border-l-2 border-orange-200 pl-2.5 leading-relaxed line-clamp-4">
          "{source.excerpt}"
        </p>
      )}

      {pdfHref && (
        <a
          href={pdfHref}
          target="_blank"
          rel="noreferrer"
          className="mt-2.5 inline-flex items-center gap-1 text-[11px] font-semibold text-orange-600 hover:text-orange-700"
        >
          <LinkIcon className="w-3 h-3" />
          View source PDF
        </a>
      )}
    </div>
  );
}

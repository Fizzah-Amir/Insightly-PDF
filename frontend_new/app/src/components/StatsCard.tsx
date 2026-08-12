import type { LucideIcon } from "lucide-react";

interface Props {
  title: string;
  value: string | number;
  icon: LucideIcon;
  accent?: "accent" | "link" | "warn";
}

const ACCENT_CLASSES = {
  accent: "bg-accent-soft text-accent",
  link: "bg-link-soft text-link",
  warn: "bg-warn-soft text-warn",
};

function StatsCard({ title, value, icon: Icon, accent = "accent" }: Props) {
  return (
    <div className="bg-surface border border-line rounded-2xl p-6 flex items-start justify-between">
      <div>
        <p className="text-sm text-ink-soft">{title}</p>
        <p className="font-mono text-3xl font-medium mt-2 text-ink tabular-nums">
          {value}
        </p>
      </div>
      <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${ACCENT_CLASSES[accent]}`}>
        <Icon size={20} strokeWidth={2} />
      </div>
    </div>
  );
}

export default StatsCard;

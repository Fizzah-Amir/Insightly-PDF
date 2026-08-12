import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  UploadCloud,
  Share2,
  MessageSquare,
} from "lucide-react";

const links = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard, end: true },
  { name: "Documents", path: "/documents", icon: FileText },
  { name: "Upload", path: "/upload", icon: UploadCloud },
  { name: "Mind map", path: "/mindmap/23", icon: Share2 },
  { name: "Chat", path: "/chat/23", icon: MessageSquare },
];

function Sidebar() {
  return (
    <aside className="w-64 shrink-0 bg-spine text-spine-text min-h-screen flex flex-col px-5 py-6">
      {/* Wordmark with the node+line signature glyph */}
      <div className="flex items-center gap-3 px-2 mb-10">
        <svg width="30" height="30" viewBox="0 0 48 48" fill="none">
          <line
            x1="15"
            y1="31"
            x2="33"
            y2="17"
            stroke="#4338ca"
            strokeWidth="3"
            strokeLinecap="round"
          />
          <circle cx="15" cy="31" r="7" fill="#4338ca" />
          <circle cx="33" cy="17" r="4.5" fill="#0e8e82" />
        </svg>
        <div>
          <h1 className="font-display font-semibold text-lg leading-none text-white">
            DocuMind
          </h1>
          <p className="text-[11px] tracking-wide uppercase text-spine-text-dim mt-1.5 font-mono">
            document workspace
          </p>
        </div>
      </div>

      <nav className="flex-1 space-y-1">
        {links.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              end={item.end}
              className={({ isActive }) =>
                `group relative flex items-center gap-3 pl-4 pr-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? "bg-white/[0.06] text-white"
                    : "text-spine-text-dim hover:text-spine-text hover:bg-white/[0.03]"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={`absolute left-0 top-1/2 -translate-y-1/2 h-4 w-[2px] rounded-full transition-colors ${
                      isActive ? "bg-accent" : "bg-transparent"
                    }`}
                  />
                  <Icon size={17} strokeWidth={2} />
                  <span className="font-medium">{item.name}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
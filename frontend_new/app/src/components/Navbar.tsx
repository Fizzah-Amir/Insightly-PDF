import { useLocation, useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { LogOut } from "lucide-react";

const TITLES: Record<string, { title: string; subtitle: string }> = {
  "/": { title: "Dashboard", subtitle: "Your AI document workspace at a glance" },
  "/documents": { title: "Documents", subtitle: "Everything you've uploaded, in one shelf" },
  "/upload": { title: "Upload", subtitle: "Add a PDF for the assistant to read" },
};

function routeMeta(pathname: string) {
  if (TITLES[pathname]) return TITLES[pathname];
  if (pathname.startsWith("/chat")) return { title: "Chat", subtitle: "Ask questions, get grounded answers" };
  if (pathname.startsWith("/mindmap")) return { title: "Mind map", subtitle: "How the ideas in this document connect" };
  return { title: "DocuMind", subtitle: "" };
}

function Navbar() {
  const { pathname } = useLocation();
  const { id } = useParams();
  const navigate = useNavigate();
  const meta = routeMeta(pathname);
  const [menuOpen, setMenuOpen] = useState(false);

  const username = localStorage.getItem("username") || "User";
  const initial = username.charAt(0).toUpperCase();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/welcome");
  };

  return (
    <header className="h-[72px] shrink-0 bg-paper/80 backdrop-blur border-b border-line flex items-center justify-between px-10 relative">
      <div>
        <h2 className="font-display text-xl font-semibold text-ink leading-tight">
          {meta.title}
          {id && (
            <span className="ml-2 align-middle text-xs font-mono font-normal text-ink-faint">
              doc #{id}
            </span>
          )}
        </h2>
        {meta.subtitle && (
          <p className="text-sm text-ink-soft mt-0.5">{meta.subtitle}</p>
        )}
      </div>

      <div className="relative">
        <button
          onClick={() => setMenuOpen((open) => !open)}
          className="flex items-center gap-3 group"
        >
          <div className="text-right">
            <p className="text-sm font-medium text-ink leading-none group-hover:text-accent transition-colors">
              {username}
            </p>
            <p className="text-xs text-ink-faint mt-1 font-mono">workspace owner</p>
          </div>
          <div className="w-9 h-9 rounded-full bg-accent text-white flex items-center justify-center font-display font-semibold text-sm">
            {initial}
          </div>
        </button>

        {menuOpen && (
          <div className="absolute right-0 top-12 bg-surface border border-line rounded-xl shadow-lg py-1.5 w-40 z-10">
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-2 px-4 py-2 text-sm text-ink hover:bg-paper transition-colors text-left"
            >
              <LogOut size={15} />
              Sign out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

export default Navbar;
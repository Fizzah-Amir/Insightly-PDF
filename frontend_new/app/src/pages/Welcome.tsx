import { useNavigate } from "react-router-dom";

function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-paper px-6">
      <div className="text-center max-w-md">
        <div className="flex justify-center mb-6">
          <svg width="44" height="44" viewBox="0 0 48 48" fill="none">
            <line
              x1="15"
              y1="31"
              x2="33"
              y2="17"
              stroke="#4338ca"
              strokeWidth="3.5"
              strokeLinecap="round"
            />
            <circle cx="15" cy="31" r="8" fill="#4338ca" />
            <circle cx="33" cy="17" r="5" fill="#0e8e82" />
          </svg>
        </div>

        <h1 className="font-display text-3xl font-semibold text-ink mb-2">
          Welcome to DocuMind
        </h1>
        <p className="text-ink-soft mb-10">
          Upload a PDF, ask it questions in plain language, and see how its
          ideas connect as a mind map.
        </p>

        <div className="flex flex-col gap-3">
          <button
            onClick={() => navigate("/signup")}
            className="w-full bg-accent hover:bg-accent-hover text-white py-3 rounded-xl font-medium text-sm transition-colors"
          >
            Create an account
          </button>
          <button
            onClick={() => navigate("/login")}
            className="w-full bg-surface border border-line hover:bg-paper-dim text-ink py-3 rounded-xl font-medium text-sm transition-colors"
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
  );
}

export default Welcome;
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/users/signup/", {
        username,
        email,
        password,
      });
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("username", response.data.username);
      navigate("/");
    } catch (err: any) {
      const msg = err.response?.data?.error || "Something went wrong. Try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-paper">
      <form
        onSubmit={handleSubmit}
        className="bg-surface p-8 rounded-2xl border border-line w-full max-w-sm"
      >
        <h1 className="font-display text-2xl font-semibold text-ink mb-1">
          Create your account
        </h1>
        <p className="text-ink-soft text-sm mb-6">
          Start building your DocuMind workspace.
        </p>

        <label className="block text-sm font-medium text-ink mb-1">
          Username
        </label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full mb-4 px-3 py-2 rounded-lg border border-line bg-paper"
          required
        />

        <label className="block text-sm font-medium text-ink mb-1">
          Email
        </label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 px-3 py-2 rounded-lg border border-line bg-paper"
        />

        <label className="block text-sm font-medium text-ink mb-1">
          Password
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 px-3 py-2 rounded-lg border border-line bg-paper"
          required
        />

        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent hover:bg-accent-hover text-white py-3 rounded-xl font-medium text-sm transition-colors"
        >
          {loading ? "Creating account…" : "Sign up"}
        </button>

        <p className="text-center text-sm text-ink-soft mt-4">
          Already have an account?{" "}
          <Link to="/login" className="text-accent font-medium">
            Sign in
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Signup;
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link to="/" className="text-lg font-semibold text-slateBrand">
          AI Resume Analyzer
        </Link>
        <nav className="flex items-center gap-4 text-sm font-medium text-slate-700">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="hover:text-accent">
                Dashboard
              </Link>
              <Link to="/upload" className="hover:text-accent">
                Upload
              </Link>
              <button
                type="button"
                onClick={onLogout}
                className="rounded-lg bg-slateBrand px-4 py-2 text-white"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-accent">
                Login
              </Link>
              <Link to="/signup" className="rounded-lg bg-slateBrand px-4 py-2 text-white">
                Sign Up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;

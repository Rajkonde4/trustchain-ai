import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export default function Navbar() {

  const navigate = useNavigate()

  const { isAuthenticated, logout } = useAuth()

  const handleLogout = () => {

    // Clear Local Storage
    localStorage.clear()

    // Auth Context Logout
    logout()

    // Redirect to Login
    navigate("/login")
  }

  return (

    <nav className="flex justify-between items-center px-8 py-5 bg-white border-b border-gray-200 sticky top-0 z-50">

      {/* LOGO */}
      <h1 className="text-2xl font-bold text-[#111827]">
        TrustChain AI
      </h1>

      {/* NAV LINKS */}
      <div className="hidden md:flex gap-10 text-gray-600 font-medium">

        <Link
          to="/"
          className="hover:text-[#3B82F6] transition"
        >
          Home
        </Link>

        <Link
          to="/upload"
          className="hover:text-[#3B82F6] transition"
        >
          Upload
        </Link>

        <Link
          to="/dashboard"
          className="hover:text-[#3B82F6] transition"
        >
          Dashboard
        </Link>

      </div>

      {/* AUTH BUTTON */}
      {

        isAuthenticated ? (

          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 transition text-white px-5 py-2 rounded-xl font-medium shadow-md"
          >

            Logout

          </button>

        ) : (

          <Link
            to="/login"
            className="bg-[#3B82F6] hover:bg-[#2563EB] transition text-white px-5 py-2 rounded-xl font-medium shadow-md"
          >

            Login

          </Link>

        )
      }

    </nav>
  )
}
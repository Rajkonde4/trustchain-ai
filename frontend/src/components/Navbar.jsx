import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth()
const navigate = useNavigate()

const handleLogout = () => {
  logout()
  navigate("/login")
}

  return (
    <nav className="flex justify-between items-center px-8 py-5 bg-white border-b border-gray-200 sticky top-0 z-50">

      <h1 className="text-2xl font-bold text-[#111827]">
        TrustChain AI
      </h1>

      <div className="hidden md:flex gap-10 text-gray-600 font-medium">

        <Link to="/" className="hover:text-[#3B82F6] transition">
          Home
        </Link>

        <Link to="/upload" className="hover:text-[#3B82F6] transition">
          Upload
        </Link>

        <Link to="/dashboard" className="hover:text-[#3B82F6] transition">
          Dashboard
        </Link>

      </div>

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
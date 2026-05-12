import Navbar from "../components/Navbar"

import { useAuth } from "../context/AuthContext"
import { useNavigate } from "react-router-dom"


export default function Login() {
 const { login } = useAuth()
const navigate = useNavigate()

const handleLogin = () => {
  login()
  navigate("/dashboard")
}
  return (
    <div className="min-h-screen bg-[#F5F7FB]">

      <Navbar />

      <div className="flex justify-center items-center pt-24 px-6">

        <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-10 border border-gray-100">

          <h1 className="text-4xl font-bold text-center text-[#111827]">
            Welcome Back
          </h1>

          <p className="text-gray-500 text-center mt-4">
            Login to continue using TrustChain AI.
          </p>

          <div className="mt-10 space-y-6">

            <input
              type="email"
              placeholder="Email Address"
              className="w-full p-4 rounded-2xl border border-gray-200 outline-none"
            />

            <input
              type="password"
              placeholder="Password"
              className="w-full p-4 rounded-2xl border border-gray-200 outline-none"
            />

            <button
              onClick={handleLogin}
              className="w-full bg-[#3B82F6] hover:bg-[#2563EB] transition text-white py-4 rounded-2xl font-medium shadow-lg"
            >
              Login
            </button>

          </div>

        </div>

      </div>

    </div>
  )
}
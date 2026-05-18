import { useState } from "react"
import { Link } from "react-router-dom"

export default function Login() {

  const [email, setEmail] = useState("")

  const [password, setPassword] = useState("")

  const [loading, setLoading] = useState(false)

  const [error, setError] = useState("")

  const handleLogin = async () => {

    // VALIDATION
    if (!email || !password) {

      setError("Please fill all fields")

      return
    }

    setLoading(true)

    setError("")

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            email,
            password
          })
        }
      )

      const data = await response.json()

      console.log(data)

      // LOGIN SUCCESS
      if (data.token) {

        // STORE TOKEN
        localStorage.setItem(
          "token",
          data.token
        )

        // STORE USER
        localStorage.setItem(
          "user",
          JSON.stringify(data.user)
        )

        // FORCE REDIRECT
        window.location.href = "/dashboard"

      } else {

        setError(
          data.message || "Invalid Credentials"
        )
      }

    } catch (error) {

      console.log(error)

      setError("Login Failed")
    }

    setLoading(false)
  }

  return (

    <div className="min-h-screen bg-[#F5F7FB] flex items-center justify-center p-6">

      <div className="bg-white shadow-2xl rounded-3xl p-10 w-full max-w-md">

        {/* HEADER */}
        <div className="text-center">

          <h1 className="text-5xl font-bold text-[#3B82F6]">
            TrustChain AI
          </h1>

          <p className="mt-4 text-gray-500">
            Secure Login Portal
          </p>

        </div>

        {/* ERROR MESSAGE */}
        {

          error && (

            <div className="mt-6 bg-red-50 border border-red-200 text-red-500 p-4 rounded-2xl text-sm">

              {error}

            </div>

          )
        }

        {/* FORM */}
        <div className="mt-10 space-y-6">

          {/* EMAIL */}
          <div>

            <label className="text-sm font-medium">
              Email
            </label>

            <input
              type="email"
              placeholder="Enter email"
              className="w-full mt-2 p-4 rounded-2xl border border-gray-300 outline-none focus:border-[#3B82F6]"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
            />

          </div>

          {/* PASSWORD */}
          <div>

            <label className="text-sm font-medium">
              Password
            </label>

            <input
              type="password"
              placeholder="Enter password"
              className="w-full mt-2 p-4 rounded-2xl border border-gray-300 outline-none focus:border-[#3B82F6]"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
            />

          </div>

          {/* LOGIN BUTTON */}
          <button
            onClick={handleLogin}
            disabled={loading}
            className="w-full bg-[#3B82F6] hover:bg-blue-600 transition-all text-white p-4 rounded-2xl font-bold text-lg"
          >

            {

              loading
                ? "Logging In..."
                : "Login"

            }

          </button>

          {/* SIGNUP LINK */}
          <div className="text-center text-gray-500 text-sm">

            Don’t have an account?

            <Link
              to="/signup"
              className="text-[#3B82F6] font-medium ml-2 hover:underline"
            >

              Create Account

            </Link>

          </div>

        </div>

      </div>

    </div>
  )
}
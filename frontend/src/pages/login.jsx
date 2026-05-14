import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Login() {

  const navigate = useNavigate()

  const [email, setEmail] = useState("")

  const [password, setPassword] = useState("")

  const [loading, setLoading] = useState(false)

  const handleLogin = async () => {

    setLoading(true)

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

      if (data.access_token) {

        localStorage.setItem(
          "token",
          data.access_token
        )

        localStorage.setItem(
          "user",
          JSON.stringify(data.user)
        )

        alert("Login Successful")

        navigate("/dashboard")

      } else {

        alert(data.message)
      }

    } catch (error) {

      console.log(error)

      alert("Login Failed")
    }

    setLoading(false)
  }

  return (

    <div className="min-h-screen bg-[#F5F7FB] flex items-center justify-center p-6">

      <div className="bg-white shadow-2xl rounded-3xl p-10 w-full max-w-md">

        <div className="text-center">

          <h1 className="text-5xl font-bold text-[#3B82F6]">
            TrustChain AI
          </h1>

          <p className="mt-4 text-gray-500">
            Secure Login Portal
          </p>

        </div>

        <div className="mt-10 space-y-6">

          <div>

            <label className="text-sm font-medium">
              Email
            </label>

            <input
              type="email"
              placeholder="Enter email"
              className="w-full mt-2 p-4 rounded-2xl border border-gray-300 outline-none"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
            />

          </div>

          <div>

            <label className="text-sm font-medium">
              Password
            </label>

            <input
              type="password"
              placeholder="Enter password"
              className="w-full mt-2 p-4 rounded-2xl border border-gray-300 outline-none"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
            />

          </div>

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

        </div>

      </div>

    </div>
  )
}
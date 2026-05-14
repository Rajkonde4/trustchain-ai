import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Signup() {

  const navigate = useNavigate()

  const [name, setName] = useState("")

  const [email, setEmail] = useState("")

  const [password, setPassword] = useState("")

  const [loading, setLoading] = useState(false)

  const handleSignup = async () => {

    setLoading(true)

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/signup",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            name,
            email,
            password
          })
        }
      )

      const data = await response.json()

      console.log(data)

      alert(data.message)

      if (
        data.message === "Signup successful"
      ) {

        navigate("/login")
      }

    } catch (error) {

      console.log(error)

      alert("Signup Failed")
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
            Create Secure Account
          </p>

        </div>

        <div className="mt-10 space-y-6">

          <div>

            <label className="text-sm font-medium">
              Name
            </label>

            <input
              type="text"
              placeholder="Enter name"
              className="w-full mt-2 p-4 rounded-2xl border border-gray-300 outline-none"
              value={name}
              onChange={(e) =>
                setName(e.target.value)
              }
            />

          </div>

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
            onClick={handleSignup}
            disabled={loading}
            className="w-full bg-[#3B82F6] hover:bg-blue-600 transition-all text-white p-4 rounded-2xl font-bold text-lg"
          >

            {
              loading
              ? "Creating Account..."
              : "Signup"
            }

          </button>

        </div>

      </div>

    </div>
  )
}
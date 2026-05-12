import Navbar from "../components/Navbar"

export default function Signup() {

  return (
    <div className="min-h-screen bg-[#F5F7FB]">

      <Navbar />

      <div className="flex justify-center items-center px-6 py-20">

        <div className="w-full max-w-md bg-white rounded-3xl border border-gray-200 shadow-xl p-10">

          <div className="text-center">

            <p className="text-[#3B82F6] uppercase tracking-[0.2em] text-sm font-semibold">
              Create Account
            </p>

            <h1 className="text-4xl font-bold mt-4 text-[#111827]">
              Join TrustChain AI
            </h1>

            <p className="text-gray-500 mt-4">
              Start verifying documents using AI-powered fraud detection.
            </p>

          </div>

          <div className="mt-10 space-y-6">

            <input
              type="text"
              placeholder="Full Name"
              className="w-full p-4 rounded-2xl border border-gray-200 outline-none focus:border-[#3B82F6]"
            />

            <input
              type="email"
              placeholder="Email Address"
              className="w-full p-4 rounded-2xl border border-gray-200 outline-none focus:border-[#3B82F6]"
            />

            <input
              type="password"
              placeholder="Password"
              className="w-full p-4 rounded-2xl border border-gray-200 outline-none focus:border-[#3B82F6]"
            />

            <button className="w-full bg-[#3B82F6] hover:bg-[#2563EB] transition text-white py-4 rounded-2xl font-medium shadow-lg">
              Create Account
            </button>

          </div>

          <p className="text-center text-gray-500 mt-8">

            Already have an account?

            <span className="text-[#3B82F6] font-medium cursor-pointer ml-2">
              Login
            </span>

          </p>

        </div>

      </div>

    </div>
  )
}
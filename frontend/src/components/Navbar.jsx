export default function Navbar() {
  return (
    <nav className="flex justify-between items-center px-8 py-4 bg-gray-900 border-b border-gray-800">
      
      <h1 className="text-2xl font-bold text-blue-500">
        TrustChain AI
      </h1>

      <div className="flex gap-6 text-white">
        <a href="/">Home</a>
        <a href="/upload">Upload</a>
        <a href="/dashboard">Dashboard</a>
        <a href="/login">Login</a>
      </div>

    </nav>
  )
}
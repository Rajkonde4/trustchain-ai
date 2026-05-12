import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "./pages/home"
import Login from "./pages/login"
import Dashboard from "./pages/dashboard"
import Upload from "./pages/upload"
import Result from "./pages/result"
import Signup from "./pages/Signup"
import ProtectedRoute from "./components/ProtectedRoute"
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
        <Route path="/upload" element={<Upload />} />
        <Route path="/result" element={<Result />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
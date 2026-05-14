import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "./pages/home"
import Login from "./pages/Login"
import Dashboard from "./pages/dashboard"
import Upload from "./pages/upload"
import Result from "./pages/result"
import Signup from "./pages/Signup"
import ProtectedRoute from "./components/ProtectedRoute"
import Verify from "./pages/Verify"

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
        <Route path="/verify/:id" element={<Verify />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
import { BrowserRouter, Routes, Route } from "react-router-dom"

import Home from "./pages/home"
import Login from "./pages/login"
import Dashboard from "./pages/dashboard"
import Upload from "./pages/upload"
import Result from "./pages/result"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
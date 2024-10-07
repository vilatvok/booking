import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import CreateService from "./pages/CreateService"
import Navigation from "./components/Navigation"
import GoogleAuth from "./pages/GoogleAuth"


function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function App() {
  return (
    <>
      <BrowserRouter>
      <Navigation />
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/google-auth" element={<GoogleAuth />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<Register />} />
          <Route path="/create-service" element={<CreateService />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
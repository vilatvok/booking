import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { UserLogin, EnterpriseLogin } from "./pages/Login"
import { UserRegister, EnterpriseRegister } from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import CreateService from "./pages/CreateService"
import Navigation from "./components/Navigation"
import GoogleAuth from "./pages/GoogleAuth"


function Logout() {
  localStorage.clear()
  return <Navigate to="/users/login" />
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
          <Route path="/users/login" element={<UserLogin />} />
          <Route path="/enterprises/login" element={<EnterpriseLogin />} />
          <Route path="/users/register" element={<UserRegister />} />
          <Route path="/enterprises/register" element={<EnterpriseRegister />} />
          <Route path="/google-auth" element={<GoogleAuth />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/create-service" element={<CreateService />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App

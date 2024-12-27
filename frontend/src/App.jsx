import { BrowserRouter, Routes, Route } from "react-router-dom";
import { UserLogin, Logout } from "./pages/Login";
import { UserRegister, CompanyRegister } from "./pages/Register";
import { PasswordReset, PasswordResetConfirm } from "./pages/PasswordReset";
import ProtectedRoute from "./components/ProtectedRoute";
import Navigation from "./components/Navigation";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import CreateOffer from "./pages/CreateOffer";
import GoogleAuth from "./pages/GoogleAuth";
import PasswordChange from "./pages/PasswordChange";
import AuthProvider from "./hooks/AuthProvider";
import Chat from "./pages/Chat";
import Settings from "./pages/Settings";


function App() {
  return (
    <>
      <BrowserRouter>
        <Navigation />
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route element={<ProtectedRoute />} >
              <Route path="/password" element={<PasswordChange />} />
              <Route path="/offers/" element={<CreateOffer />} />
              <Route path="/chats/:chat_id" element={<Chat />} />
              <Route path="/users/:name" element={<Profile />}/>
              <Route path="/companies/:name" element={<Profile />}/>
              <Route path="/logout" element={<Logout />} />
              <Route path="/settings" element={<Settings />} />
            </Route>
            <Route path="/auth/login" element={<UserLogin />} />
            <Route path="/auth/register" element={<UserRegister />} />
            <Route
              path="/companies/register"
              element={<CompanyRegister />}
            />
            <Route path="/auth/google-auth" element={<GoogleAuth />} />
            <Route path="/password-reset" element={<PasswordReset />} />
            <Route path="/password-reset/:token" element={<PasswordResetConfirm />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
}

export default App;

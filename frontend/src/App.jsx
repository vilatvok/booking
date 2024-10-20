import { BrowserRouter, Routes, Route } from "react-router-dom";
import { UserLogin, EnterpriseLogin, Logout } from "./pages/Login";
import { UserRegister, EnterpriseRegister } from "./pages/Register";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import CreateService from "./pages/CreateService";
import Navigation from "./components/Navigation";
import GoogleAuth from "./pages/GoogleAuth";
import PasswordChange from "./pages/PasswordChange";
import AuthProvider from "./hooks/AuthProvider";
import Chat from "./pages/Chat";
import { PasswordReset, PasswordResetConfirm } from "./pages/PasswordReset";


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
              <Route path="/create-service" element={<CreateService />} />
              <Route path="/chats/:chat_id" element={<Chat />} />
              <Route path="/users/:name" element={<Profile />}/>
              <Route path="/enterprises/:name" element={<Profile />}/>
            </Route>
            <Route path="/users/login" element={<UserLogin />} />
            <Route path="/enterprises/login" element={<EnterpriseLogin />} />
            <Route path="/users/register" element={<UserRegister />} />
            <Route
              path="/enterprises/register"
              element={<EnterpriseRegister />}
            />
            <Route path="/google-auth" element={<GoogleAuth />} />
            <Route path="/password-reset" element={<PasswordReset />} />
            <Route path="/password-reset/:token" element={<PasswordResetConfirm />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
}

export default App;

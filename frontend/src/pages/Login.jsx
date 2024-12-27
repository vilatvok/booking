import HandleForm from "../components/AuthForm";
import { Navigate } from "react-router-dom";


export function UserLogin() {
  return <HandleForm route="/auth/login" method="login" />;
}

export function Logout() {
  localStorage.clear();
  return <Navigate to="/auth/login" />;
}

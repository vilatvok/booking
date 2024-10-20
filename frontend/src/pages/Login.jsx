import HandleForm from "../components/AuthForm";
import { Navigate } from "react-router-dom";


export function UserLogin() {
  return <HandleForm route="/users/login" method="login" />;
}

export function EnterpriseLogin() {
  return <HandleForm route="/enterprises/login" method="login" />;
}

export function Logout() {
  localStorage.clear();
  return <Navigate to="/users/login" />;
}

import HandleForm from "../components/AuthForm";
import { useLocation } from "react-router-dom";


export function UserRegister() {
  const location = useLocation();
  if (location.state.googleData) {
    return (
      <HandleForm
        route="/auth/google-auth/register"
        method="register"
        googleData={location.state.googleData}
      />
    );
  } else {
    return (
      <HandleForm 
        route="/auth/register"
        method="register" 
      />
    );
  }
}


export function CompanyRegister() {
  return (
    <HandleForm
      route="/companies/register"
      method="register"
      googleData={null}
    />
  );
}

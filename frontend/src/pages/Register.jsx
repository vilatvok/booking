import HandleForm from "../components/AuthForm";

import { useLocation } from "react-router-dom";

export function UserRegister() {
  const location = useLocation();
  if (location.state) {
    return (
      <HandleForm
        route="/google-auth/register"
        method="register"
        googleData={location.state.googleData}
      />
    );
  } else {
    return (
      <HandleForm route="/users/register" method="register" googleData={null} />
    );
  }
}

export function EnterpriseRegister() {
  return (
    <HandleForm
      route="/enterprises/register"
      method="register"
      googleData={null}
    />
  );
}

import { useEffect } from "react";
import { useAuth } from "../hooks/AuthProvider";
import { Navigate, useSearchParams } from "react-router-dom";


function GoogleAuth() {
  const auth = useAuth();
  const [params] = useSearchParams();

  useEffect(() => {
    authAction();
  }, []);

  const authAction = async () => {
    const is_param = params.get("code");
    if (is_param !== null) {
      let url = "/auth/google-auth/login?code=" + is_param;
      await auth.googleLogin(url)
    }
  };

  // Redirect after auth is complete
  if (auth.token) {
    return <Navigate to="/" />
  }

  return <div>Authenticating with Google...</div>

}

export default GoogleAuth;

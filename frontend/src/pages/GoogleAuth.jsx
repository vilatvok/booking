import { useEffect, useState } from "react";
import { Navigate, useSearchParams, useNavigate } from "react-router-dom";

import api from "../utils/api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";


function GoogleAuth() {
  const [params] = useSearchParams();
  const [authCompleted, setAuthCompleted] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    auth();
  }, []);

  const auth = async () => {
    const is_param = params.get('code');
    if (is_param !== null) {
      let url = "/google-auth/login?code=" + is_param;
      try {
        const res = await api.get(url);
        if (res.data.access_token) {
          localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
          localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        } else if (res.data.url) {
          navigate("/register", { state: { googleData: res.data } });
          return;  // Prevent further execution after navigating
        }
      } catch (err) {
        console.log(err);
      }
    }
    setAuthCompleted(true);  // Set state after auth is complete
  };

  // Redirect after auth is complete
  if (authCompleted) {
    return <Navigate to="/" />;
  }

  return <div>Authenticating...</div>;  // Display while waiting for auth to complete
}


export default GoogleAuth;

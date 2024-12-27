import api from "../utils/api";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/AuthProvider";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../data/constants";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ProtectedRoute() {
  const { token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    auth();
  }, []);

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
    try {
      const res = await api.post("auth/token/refresh", {
        refresh_token: refreshToken,
      });
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
      } else {
        localStorage.clear();
      }
    } catch (error) {
      console.log(error);
      localStorage.clear();
    }
  };

  const auth = async () => {
    if (!token) {
      return;
    }
    const time_exp = token.exp;
    const now = Date.now() / 1000;

    if (time_exp < now) {
      await refreshToken();
      return;
    }
    const username = token.username;
    const userExists = await api
      .get(`users/${username}`)
      .then((res) => res.status)
      .catch((err) => console.log(err));
    
    if (userExists !== 200) {
      navigate("/auth/login");
    }
  };

  return token ? <Outlet /> : <Navigate to="/auth/login" />;
}

export default ProtectedRoute;

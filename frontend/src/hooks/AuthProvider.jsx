import api from "../utils/api";
import { useState, createContext, useContext } from "react";
import { useCurrentUser } from "./useCurrentUser";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";


const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

function AuthProvider({ children }) {
  const user = useCurrentUser();
  const [token, setToken] = useState(user);
  const navigate = useNavigate();

  const login = async (route, data) => {
    await api
      .post(route, data)
      .then((res) => {
        if (res.status === 200) {
          const access_token = res.data.access_token;
          const decoded = jwtDecode(access_token);

          localStorage.setItem(ACCESS_TOKEN, access_token);
          localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);

          setToken(decoded);
          navigate("/");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const googleLogin = async (route) => {
    await api
      .get(route)
      .then((res) => {
        if (res.status === 200 && res.data.access_token) {
          const access_token = res.data.access_token;
          const decoded = jwtDecode(access_token);

          // Store tokens in local storage
          localStorage.setItem(ACCESS_TOKEN, access_token);
          localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);

          setToken(decoded);
        } else if (res.status === 200 && res.data.url) {
          const googleData = {
            email: res.data.email,
            google_id: res.data.google_id,
            avatar: res.data.avatar,
          }
          navigate("/auth/register", { state: { googleData } });
        }
      })
      .catch((err) => { console.log(err) });
  };

  const register = async (route, data) => {
    await api
    .post(route, data)
    .then((res) => {
      if ([200, 201].includes(res.status)) {
        navigate("/auth/login");
      }
    })
    .catch((err) => {
      console.log(err);
    });
  }

  return (
    <AuthContext.Provider value={{ token, login, googleLogin, register }}>
      {children}
    </AuthContext.Provider>
  );
}


export default AuthProvider;

import api from '../utils/api';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { REFRESH_TOKEN, ACCESS_TOKEN } from '../data/constants';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';


function ProtectedRoute({ children }) {
  const [authorized, setAuthorized] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    auth().catch(() => setAuthorized(true))
  }, []);

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
    try {
      const res = await api.post("users/token/refresh", {
        refresh: refreshToken,
      });
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        setAuthorized(true);
      } else {
        setAuthorized(false);
      }
    } catch (error) {
      console.log(error);
      setAuthorized(false);
    }
  };

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    console.log(token)
    if (!token) {
      setAuthorized(false);
      return;
    }
  
    // check if the user is logged in
    const decoded = jwtDecode(token);
    const time_exp = decoded.exp;
    const now = Date.now() / 1000;
    if (time_exp < now) {
      await refreshToken();
    } else {
      const isUser = (
        await api
          .get(`users/${decoded.username}`)
          .then((res) => res.status)
          .catch((err) => console.log(err))
      )
      if (isUser === 200) {
        setAuthorized(true);
      } else {
        console.log('hasa')
        navigate("/login");
      }
    }
  };

  if (authorized === null) {
    return <div>Loading...</div>;
  }
  return authorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;

import api from '../utils/api';
import { Navigate } from 'react-router-dom';
import { REFRESH_TOKEN, ACCESS_TOKEN } from '../data/constants';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCurrentObj } from '../hooks/useCurrentObject';


function ProtectedRoute({ children }) {
  const [authorized, setAuthorized] = useState(null);
  const authenticatedObject = useCurrentObj();
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
    if (!authenticatedObject) {
      setAuthorized(false);
      return;
    }
    const time_exp = authenticatedObject.exp;
    const now = Date.now() / 1000;
    if (time_exp < now) {
      await refreshToken();
    } else {
      const objName = authenticatedObject.name;
      const objType = authenticatedObject.obj;
      const url = objType === 'user' ? `users/${objName}` : `enterprises/${objName}`;
      const isObj = (
        await api
          .get(url)
          .then((res) => res.status)
          .catch((err) => console.log(err))
      )
      if (isObj === 200) {
        setAuthorized(true);
      } else {
        navigate("/users/login");
      }
    }
  };

  if (authorized === null) {
    return <div>Loading...</div>;
  }
  return authorized ? children : <Navigate to="/users/login" />;
}

export default ProtectedRoute;

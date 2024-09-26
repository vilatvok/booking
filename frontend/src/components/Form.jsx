import api from "../utils/api";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";


function HandleForm({ route, method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const form = new FormData();
      if (method === 'register') {
        const user = {
          'username': username,
          'email': email,
          'password': password,
        }
        form.append('user', JSON.stringify(user))
        console.log(form)
      } else {
        form.append('username', username)
        form.append('password', password)
      }

      const res = await api.post(route, form);
  
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        navigate('/');
      } else {
        navigate('/login');
      }
    } catch (error) {
      console.log(error.response)
    }
  }

  const name = method === "login" ? "Login" : "Register"

  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
          </div>
          {method == "register" &&
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Email
              </label>
              <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="email" type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
            </div>
          }
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="******************" onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-teal-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
              {name}
            </button>
            <a className="inline-block align-baseline font-bold text-sm text-teal-500 hover:text-blue-800" href="#">
              Forgot Password?
            </a>
          </div>
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Acme Corp. All rights reserved.
        </p>
      </div>
    </div>
  )
}

export default HandleForm

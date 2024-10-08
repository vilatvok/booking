import api from "../utils/api";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";


function UserLogin({ form }) {
  const { setUsername, setPassword, handleSubmit, googleAuth, setFormType } = form;
  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
          leading-tight focus:outline-none focus:shadow-outline"
              id="username" type="text" placeholder="Username"
              onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 
          leading-tight focus:outline-none focus:shadow-outline"
              id="password" type="password" placeholder="********"
              onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
          font-bold py-2 px-4 rounded 
          focus:outline-none focus:shadow-outline" type="submit">
              Login
            </button>
            
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
          font-bold py-2 px-4 rounded 
          focus:outline-none focus:shadow-outline"
              onClick={googleAuth}>
              Google
            </button>
          </div>
          <div className="mt-4 flex items-center justify-center">
            <a
              href="/enterprises/login"
              className="text-primary focus:outline-none dark:text-primary-400"
              onClick={() => setFormType('enterprise')}
            >
              Login as an enterprise?
            </a>
          </div>
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Kovtaliv Corp. All rights reserved.
        </p>
      </div>
    </div>
  )
}


function EnterpriseLogin({ form }) {
  const { setUsername, setPassword, handleSubmit } = form;
  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
          leading-tight focus:outline-none focus:shadow-outline"
              id="email" type="text" placeholder="Email"
              onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 
          leading-tight focus:outline-none focus:shadow-outline"
              id="password" type="password" placeholder="********"
              onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
                font-bold py-2 px-4 rounded 
                focus:outline-none focus:shadow-outline" 
                type="submit">
              Login
            </button>
          </div>
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Kovtaliv Corp. All rights reserved.
        </p>
      </div>
    </div>
  )
}


function UserRegister({ form }) {
  const { setUsername, setEmail, setPassword, handleSubmit, googleAuth, setFormType } = form;

  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
              leading-tight focus:outline-none focus:shadow-outline"
              id="username" type="text" placeholder="Username"
              onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input className="shadow appearance-none border rounded 
              w-full py-2 px-3 text-gray-700 leading-tight 
              focus:outline-none focus:shadow-outline"
              id="email" type="email" placeholder="Email"
              onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 
              leading-tight focus:outline-none focus:shadow-outline"
              id="password" type="password" placeholder="********"
              onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 rounded 
              focus:outline-none focus:shadow-outline" type="submit">
              Register
            </button>
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 rounded 
              focus:outline-none focus:shadow-outline"
              onClick={googleAuth}>
              Google
            </button>
          </div>
          <div className="mt-4 flex items-center justify-center">
            <a
              href="/enterprises/register"
              className="text-primary focus:outline-none dark:text-primary-400"
              onClick={() => setFormType('enterprise')}
            >
              Register as an enterprise?
            </a>
          </div>
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Kovtaliv Corp. All rights reserved.
        </p>
      </div>
    </div>
  );
}


function EnterpriseRegister({ form }) {
  const { setName, setOwner, setEmail, setPassword, handleSubmit } = form;
  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
              Name
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
          leading-tight focus:outline-none focus:shadow-outline"
              id="name" type="text" placeholder="Name"
              onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="owner">
              Owner
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
          leading-tight focus:outline-none focus:shadow-outline"
              id="owner" type="text" placeholder="Owner"
              onChange={(e) => setOwner(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input className="shadow appearance-none border rounded 
          w-full py-2 px-3 text-gray-700 leading-tight 
          focus:outline-none focus:shadow-outline"
              id="email" type="email" placeholder="Email"
              onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 
        leading-tight focus:outline-none focus:shadow-outline"
              id="password" type="password" placeholder="********"
              onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-teal-500 hover:bg-blue-700 text-white 
          font-bold py-2 px-4 rounded 
          focus:outline-none focus:shadow-outline" type="submit">
              Register
            </button>
          </div>
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Kovtaliv Corp. All rights reserved.
        </p>
      </div>
    </div>
  )
}

function HandleForm({ route, method, googleData }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // google data
  const [googleId, setGoogleId] = useState("");

  // enterprise data
  const [name, setName] = useState("");
  const [owner, setOwner] = useState("");

  // Manage form type (user or enterprise)
  const [formType, setFormType] = useState('user'); // default is 'user'

  useEffect(() => {
    if (googleData) {
      if (googleData.email && googleData.google_id) {
        setEmail(googleData.email);
        setGoogleId(googleData.google_id);
      }
    }
  }, [googleData]);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const form = new FormData();
      let obj;
      switch (method) {
        case "login":
          form.append('username', username);
          form.append('password', password);
          await api.post(route, form)
            .then((res) => {
              if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
                navigate('/');
              }
            })
            .catch((err) => { console.log(err); });
          break;
        case "register":
          if (googleId) {
            obj = {
              'username': username,
              'email': email,
              'social_id': googleId,
            };
          } else if (route === "/enterprises/register") {
            obj = {
              'name': name,
              'owner': owner,
              'email': email,
              'password': password,
            };
          } else {
            obj = {
              'username': username,
              'email': email,
              'password': password,
            };
          }
          form.append('form', JSON.stringify(obj));
          await api.post(route, form)
            .then((res) => {
              if (res.status === 200) {
                if (formType === 'enterprise') {
                  navigate("/enterprises/login");
                } else {
                  navigate("/users/login");
                }
              }
            })
            .catch((err) => { console.log(err); });
          break;
        default:
          break;
      }
    } catch (error) {
      console.log(error.response);
    }
  };

  const googleAuth = async () => {
    await api.get('/google-auth/signin')
      .then((res) => { window.location.href = res.data.url; })
      .catch((err) => { console.log(err); });
  };

  let formComponent;
  switch (route) {
    case '/enterprises/register':
      formComponent = <EnterpriseRegister form={{ setName, setOwner, setEmail, setPassword, handleSubmit }} />;
      break;
    case '/enterprises/login':
      formComponent = <EnterpriseLogin form={{ setUsername, setPassword, handleSubmit }} />;
      break;
    case '/users/register':
      formComponent = <UserRegister form={{ setUsername, setEmail, setPassword, handleSubmit, googleAuth, setFormType }} />;
      break;
    default:
      formComponent = <UserLogin form={{ setUsername, setPassword, handleSubmit, googleAuth, setFormType }} />;
      break
  } 
  return formComponent;
}

export default HandleForm;

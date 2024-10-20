import api from "../utils/api";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";


export function PasswordReset() {
  const [email, setEmail] = useState("");
  const [objType, setObjType] = useState("user");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      model: objType,
      email: email,
    }
    await api
      .post('/auth/password-reset', data)
      .then((res) => {
        if (res.status === 202) {
          console.log("Email sent");
          navigate("/users/login");
        }
      })
      .catch((err) => { console.error("Error:", err) });
  }

  return (
    <div className="m-5">
      <form className="w-full max-w-lg" onSubmit={handleSubmit}>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700
              text-xs font-bold mb-2"
              htmlFor="email"
            >
              Email:
            </label>
            <input
              onChange={(e) => setEmail(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
              border-gray-200 rounded py-3 px-4 leading-tight 
              focus:outline-none focus:bg-white focus:border-gray-500"
              id="email"
              type="text"
              placeholder="email"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="type"
            >
              Type:
            </label>
            <div className="relative">
              <select
                value={objType}
                onChange={(e) => setObjType(e.target.value)}
                className="block appearance-none w-full bg-gray-200 border border-gray-200 
                text-gray-700 py-3 px-4 pr-8 rounded leading-tight 
                focus:outline-none focus:bg-white focus:border-gray-500"
                id="type"
              >
                <option>user</option>
                <option>enterprise</option>
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                <svg
                  className="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <button
              type="submit"
              className="focus:outline-none text-white 
              bg-teal-500 hover:bg-teal-600 focus:ring-4 focus:ring-green-300
              font-medium rounded-lg text-sm px-5 py-2.5
              me-2 mb-2 dark:bg-teal-500 
              dark:hover:bg-teal-600 
              dark:focus:ring-green-800"
            >
              Save
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export function PasswordResetConfirm() {
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const { token } = useParams();
  const navigate = useNavigate();
  console.log(token)

  const handleSubmit = async (e) => {
    e.preventDefault();

    await api
      .patch(`/auth/password-reset/${token}`, { password1, password2 })
      .then((res) => {
        if (res.status === 200) {
          console.log("Password updated");
          navigate("/users/login");
        }
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  };

  return (
    <div className="m-5">
      <form className="w-full max-w-lg" onSubmit={handleSubmit}>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700
              text-xs font-bold mb-2"
              htmlFor="password"
            >
              Password:
            </label>
            <input
              onChange={(e) => setPassword1(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
              border-gray-200 rounded py-3 px-4 leading-tight 
              focus:outline-none focus:bg-white focus:border-gray-500"
              id="password"
              type="password"
              placeholder="password1"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700
              text-xs font-bold mb-2"
              htmlFor="password2"
            >
              Repeat password:
            </label>
            <input
              onChange={(e) => setPassword2(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
              border-gray-200 rounded py-3 px-4 leading-tight 
              focus:outline-none focus:bg-white focus:border-gray-500"
              id="password2"
              type="password"
              placeholder="password2"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <button
              type="submit"
              className="focus:outline-none text-white 
              bg-teal-500 hover:bg-teal-600 focus:ring-4 focus:ring-green-300
              font-medium rounded-lg text-sm px-5 py-2.5
              me-2 mb-2 dark:bg-teal-500 
              dark:hover:bg-teal-600 
              dark:focus:ring-green-800"
            >
              Save
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

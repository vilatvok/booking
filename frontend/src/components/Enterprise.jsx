import api from "../utils/api";
import { useEffect, useState } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";
import { useNavigate } from "react-router-dom";

function Enterprise({ enterprise, onUpdate }) {
  const [name, setName] = useState("");
  const [owner, setOwner] = useState("");
  const [email, setEmail] = useState("");
  const [logo, setLogo] = useState(null);
  const [editing, setEditing] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    setName(enterprise.name);
    setEmail(enterprise.email);
    setOwner(enterprise.owner);
  }, [enterprise]);

  // get tokens
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);

  const editEnterprise = async (event) => {
    event.preventDefault();

    // generate form data
    const formData = new FormData();
    if (owner) {
      formData.append("owner", owner);
    }
    if (name) {
      formData.append("name", name);
    }
    if (email) {
      formData.append("email", email);
    }
    if (logo) {
      formData.append("logo", logo);
    }
    // send request
    const res = await api
      .patch(`/enterprises/me`, formData)
      .then((res) => res.status)
      .catch((err) => console.log(err.response));

    if (res === 202) {
      if (name !== enterprise.name) {
        const tokenData = {
          refresh_token: refreshToken,
          enterprise: name,
        };
        await api
          .post("/auth/token/refresh", tokenData)
          .then((res) => {
            if (res.status === 200) {
              localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
              localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
            }
          })
          .catch((err) => console.log(err));
      }
      onUpdate(name);
      setEditing(false);
    }
  };

  return (
    <div className="max-w-sm w-full lg:max-w-full lg:flex m-5">
      <div
        className="h-48 lg:h-48 lg:w-48 flex-none bg-cover 
        rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden"
        style={{
          backgroundImage: `url(http://localhost:8000/${enterprise.logo})`,
        }}
      ></div>
      <div
        className="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t 
        lg:border-gray-400 bg-gray-900 rounded-b lg:rounded-b-none dark:text-white
        lg:rounded-r p-4 flex flex-col justify-between leading-tight"
      >
        <div className="mb-8">
          <div className="font-bold text-xl mb-2">
            {enterprise.name}
          </div>
          <p className="text-base">{enterprise.email}</p>
        </div>
        <div className="flex">
          <button
            onClick={() => setEditing(!editing)}
            className="inline-flex items-center px-3 py-2 text-sm font-medium 
            text-center text-white bg-teal-500
            rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
            focus:ring-blue-300 dark:bg-teal-500
            dark:hover:bg-teal-600 dark:focus:ring-blue-800"
          >
            Edit
            <svg
              className="rtl:rotate-180 w-3.5 h-3.5 ms-2"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 10"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M1 5h12m0 0L9 1m4 4L9 9"
              />
            </svg>
          </button>
          <button
            onClick={() => navigate("/create-service")}
            className="ms-2 inline-flex items-center px-3 py-2 text-sm 
            font-medium text-center text-white bg-teal-500
            rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
            focus:ring-blue-300 dark:bg-teal-500
            dark:hover:bg-teal-600 dark:focus:ring-blue-800"
          >
            Add
            <svg
              className="rtl:rotate-180 w-3.5 h-3.5 ms-2"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 10"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M1 5h12m0 0L9 1m4 4L9 9"
              />
            </svg>
          </button>
        </div>
        {editing && (
          <form className="max-w-sm mx-auto">
            <div className="mb-2 mt-2">
              <label
                htmlFor="avatar"
                className="block mb-2 text-sm font-medium text-gray-900"
              >
                Name
              </label>
              <input
                type="username"
                id="username"
                className="bg-gray-50 border border-gray-300 
                text-gray-900 text-sm rounded-lg 
                focus:ring-blue-500 focus:border-blue-500 block w-full 
                p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 
                dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="username"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="mb-2">
              <label
                htmlFor="email"
                className="block mb-2 text-sm font-medium text-gray-900"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg 
                focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 
                dark:border-gray-600 dark:placeholder-gray-400 dark:text-white 
                dark:focus:ring-blue-500 dark:focus:border-blue-500"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="mb-2">
              <label
                htmlFor="avatar"
                className="ms-2 text-sm font-medium text-gray-900"
              >
                Avatar
              </label>
              <input
                id="avatar"
                type="file"
                onChange={(e) => setLogo(e.target.files[0])}
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg 
                focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 
                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 
                dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              />
            </div>
            <button
              onClick={editEnterprise}
              className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 
              focus:outline-none focus:ring-blue-300 font-medium rounded-lg 
              text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 
              dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Submit
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default Enterprise;

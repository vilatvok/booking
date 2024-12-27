import api from "../utils/api";
import { useEffect, useState } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";
import { useNavigate } from "react-router-dom";
import { useCurrentUser } from "../hooks/useCurrentUser";


function User({ user, onUpdate }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [avatar, setAvatar] = useState(null);
  const [editing, setEditing] = useState(false);
  const currUser = useCurrentUser().username;
  const navigate = useNavigate();
  const isCurrUser = currUser === user.username;
  const avatarUrl = encodeURI(`http://localhost:8000/${user.avatar}`);

  useEffect(() => {
    setUsername(user.username);
    setEmail(user.email);
  }, [user]);

  // get tokens
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);

  const editUser = async (event) => {
    event.preventDefault();

    // generate form data
    const formData = new FormData();
    if (username) {
      formData.append("username", username);
    }
    if (email) {
      formData.append("email", email);
    }
    if (avatar) {
      formData.append("avatar", avatar);
    }
    // send request
    const res = await api
      .patch(`/users/me`, formData)
      .then((res) => res.status)
      .catch((err) => console.log(err.response));

    if (res === 202) {
      if (username !== user.username) {
        const tokenData = {
          refresh_token: refreshToken,
          username: username,
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
      onUpdate(username);
      setEditing(false);
    }
  };

  const handleChatRedirect = async () => {
    await api
      .get("/chats/id", { params: { user_id: user.id } })
      .then(async (res) => {
        if (res.status === 200) {
          await api
            .get(`/chats/${res.data}`)
            .then((res) => navigate(`/chats/${res.data.id}`))
            .catch((err) => console.log(err));
        }
      })
      .catch(async (err) => {
        await api
          .post("/chats", { user_id: user.id })
          .then((res) => {
            console.log(res.data)
            navigate(`/chats/${res.data}`)
          })
          .catch((err) => console.log(err));
      });
  }

  return (
    <div className="max-w-sm w-full lg:max-w-full lg:flex">
      <div
        className="h-48 lg:h-48 lg:w-48 flex-none bg-cover 
        rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden"
        style={{ backgroundImage: `url('${avatarUrl}')` }}
      ></div>
      <div
        className="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t 
        lg:border-gray-400 bg-gray-900 rounded-b lg:rounded-b-none dark:text-white
        lg:rounded-r p-4 flex flex-col justify-between leading-tight"
      >
        <div className="mb-8">
          <div className="font-bold text-xl mb-2">{user.username}</div>
          <p className="text-base">{user.email}</p>
        </div>
        <div className="flex">
          {isCurrUser ? (
            <>
              <button
                onClick={() => navigate('/settings/')}
                className="inline-flex items-center px-3 py-2 text-sm font-medium 
                text-center text-white bg-teal-500
                rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
                focus:ring-blue-300 dark:bg-teal-500
                dark:hover:bg-teal-600 dark:focus:ring-blue-800"
              >
                Settings
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
                onClick={() => setEditing(!editing)}
                className="ms-2 inline-flex items-center px-3 py-2 text-sm font-medium 
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
                onClick={() => navigate("/offers")}
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
              <button
                onClick={() => navigate("/password")}
                className="ms-2 inline-flex items-center px-3 py-2 text-sm 
                font-medium text-center text-white bg-teal-500
                rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
                focus:ring-blue-300 dark:bg-teal-500
                dark:hover:bg-teal-600 dark:focus:ring-blue-800"
              >
                Password
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
            </>
          ) : (
            <button
              onClick={handleChatRedirect}
              className="inline-flex items-center px-3 py-2 text-sm font-medium 
              text-center text-white bg-teal-500
              rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
              focus:ring-blue-300 dark:bg-teal-500
              dark:hover:bg-teal-600 dark:focus:ring-blue-800"
            >
              Message
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
          )}
        </div>
        {editing && (
          <form className="max-w-sm mx-auto">
            <div className="mb-2 mt-2">
              <label
                htmlFor="avatar"
                className="block mb-2 text-sm font-medium text-gray-900"
              >
                Username
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
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
                onChange={(e) => setAvatar(e.target.files[0])}
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg 
                focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 
                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 
                dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              />
            </div>
            <button
              onClick={editUser}
              className="text-white bg-teal-500 hover:bg-teal-600 focus:ring-4 
              focus:outline-none focus:ring-blue-300 font-medium rounded-lg 
              text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-teal-500
              dark:hover:bg-teal-600 dark:focus:ring-blue-800"
            >
              Submit
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default User;

import api from "../utils/api";
import { useEffect, useState } from "react";
import { useAuth } from "../hooks/AuthProvider";

function AuthForm({
  fields,
  handleSubmit,
  methodType,
  googleAuth,
}) {
  return (
    <div className="flex items-center justify-center mt-8">
      <div className="w-full max-w-xs">
        <form
          className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
          onSubmit={handleSubmit}
        >
          {fields.map((field) => (
            <div className="mb-4" key={field.id}>
              <label
                className="block text-gray-700 text-sm font-bold mb-2"
                htmlFor={field.id}
              >
                {field.label}
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 
                leading-tight focus:outline-none focus:shadow-outline"
                id={field.id}
                type={field.type}
                placeholder={field.placeholder}
                onChange={field.onChange}
                value={field.value}
                disabled={field.disabled}
              />
            </div>
          ))}
          <div className="flex items-center justify-between">
            <button
              className="bg-teal-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 rounded 
              focus:outline-none focus:shadow-outline"
              type="submit"
            >
              {methodType === "register" ? "Register" : "Login"}
            </button>
            <button
              className="bg-teal-500 hover:bg-blue-700 text-white 
              font-bold py-2 px-4 rounded 
              focus:outline-none focus:shadow-outline"
              onClick={googleAuth}
            >
              Google
            </button>
          </div>
          {methodType === "login" && (
            <div className="mt-4 flex items-center justify-center">
              <a
                href="/password-reset"
                className="ms-2 text-primary focus:outline-none dark:text-primary-400"
              >
                Forgot password?
              </a>
            </div>
          )}
        </form>
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Kovtaliv Corp. All rights reserved.
        </p>
      </div>
    </div>
  );
}


function HandleForm({ route, method, googleData }) {
  const auth = useAuth();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [avatar, setAvatar] = useState(null);

  // google data
  const [googleId, setGoogleId] = useState("");
  const [methodType, setMethodType] = useState(null);

  useEffect(() => {
    if (googleData) {
      if (googleData.email && googleData.google_id && googleData.avatar) {
        setEmail(googleData.email);
        setGoogleId(googleData.google_id);
        setAvatar(googleData.avatar);
      }
    }
  }, [googleData]);

  useEffect(() => {
    if (method === "login") {
      setMethodType("login");
    } else {
      setMethodType("register");
    }
  }, [method, route]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const form_data = new FormData();
      form_data.append("username", username);

      switch (method) {
        case "login":
          form_data.append("password", password);
          if (username !== "" && password !== "") {
            auth.login(route, form_data);
          }
          break;
        case "register":
          form_data.append("email", email);
          if (avatar) form_data.append("avatar", avatar);
          if (googleId) {
            form_data.append('social_id', googleId);
          } else {
            form_data.append('password', password);
          }

          // only specific case for user registration
          if (username !== "" && email !== "" && password !== "") {
            auth.register(route, form_data);
          }
          break;
        default:
          break;
      }
    } catch (error) {
      console.log(error.response);
    }
  };

  const googleAuth = async () => {
    await api
      .get("/auth/google-auth/link")
      .then((res) => {
        window.location.href = res.data.url;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const fields = [];

  fields.push(
    {
      id: "username",
      label: "Username",
      type: "text",
      placeholder: "Username",
      onChange: (e) => setUsername(e.target.value),
    },
    {
      id: "password",
      label: "Password",
      type: "password",
      placeholder: "********",
      onChange: (e) => setPassword(e.target.value),
    }
  );

  console.log(route)
  if (route === "/auth/register") {
    fields.push(
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "Email",
        onChange: (e) => setEmail(e.target.value),
      },
      {
        id: "avatar",
        label: "Avatar",
        type: "file",
        onChange: (e) => setAvatar(e.target.files[0]),
      }
    );
  }
  if (googleId) {
    fields.push(
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "Email",
        value: email,
        disabled: true,
      },
    );
  }

  return (
    <AuthForm
      fields={fields}
      handleSubmit={handleSubmit}
      methodType={methodType}
      googleAuth={googleAuth}
    />
  );
}

export default HandleForm;

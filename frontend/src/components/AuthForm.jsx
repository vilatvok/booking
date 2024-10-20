import api from "../utils/api";
import { useEffect, useState } from "react";
import { useAuth } from "../hooks/AuthProvider";

function AuthForm({
  fields,
  handleSubmit,
  formType,
  setFormType,
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
            {formType === "user" && (
              <button
                className="bg-teal-500 hover:bg-blue-700 text-white 
                font-bold py-2 px-4 rounded 
                focus:outline-none focus:shadow-outline"
                onClick={googleAuth}
              >
                Google
              </button>
            )}
          </div>
          {methodType === "login" && (
            <div className="mt-4 flex items-center justify-center">
              <a
                href={
                  formType === "user" ? "/users/login" : "/enterprises/login"
                }
                className="text-primary focus:outline-none dark:text-primary-400"
                onClick={() =>
                  setFormType(formType === "user" ? "enterprise" : "user")
                }
              >
                {formType === "user"
                  ? "Login as an enterpise?"
                  : "Login as a user?"}
              </a>
              <a
                href="/password-reset"
                className="ms-2 text-primary focus:outline-none dark:text-primary-400"
              >
                Forgot password?
              </a>
            </div>
          )}
          {methodType === "register" && (
            <div className="mt-4 flex items-center justify-center">
              <a
                href={
                  formType === "user"
                    ? "/users/register"
                    : "/enterprises/register"
                }
                className="text-primary focus:outline-none dark:text-primary-400"
                onClick={() =>
                  setFormType(formType === "user" ? "enterprise" : "user")
                }
              >
                {formType === "user"
                  ? "Register as an enterprise?"
                  : "Register as a user?"}
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

  // enterprise data
  const [name, setName] = useState("");
  const [owner, setOwner] = useState("");

  const [formType, setFormType] = useState(null);
  const [methodType, setMethodType] = useState(null);

  useEffect(() => {
    if (googleData) {
      if (googleData.email && googleData.google_id) {
        setEmail(googleData.email);
        setGoogleId(googleData.google_id);
      }
    }
  }, [googleData]);

  useEffect(() => {
    if (method === "login") {
      setMethodType("login");
    } else {
      setMethodType("register");
    }

    if (route.includes("users")) {
      setFormType("user");
    } else {
      setFormType("enterprise");
    }
  }, [method, route]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const form = new FormData();
      let obj;
      switch (method) {
        case "login":
          form.append("username", username);
          form.append("password", password);
          if (username !== "" && password !== "") {
            auth.login(route, form);
          }
          break;
        case "register":
          if (googleId) {
            obj = {
              username: username,
              email: email,
              social_id: googleId,
            };
            if (avatar) form.append("avatar", avatar);
          } else if (route === "/enterprises/register") {
            obj = {
              name: name,
              owner: owner,
              email: email,
              password: password,
            };
            if (avatar) form.append("logo", avatar);
          } else {
            obj = {
              username: username,
              email: email,
              password: password,
            };
            if (avatar) form.append("avatar", avatar);
          }
          form.append("form", JSON.stringify(obj));

          // only specific case for user registration
          if (username !== "" && email !== "" && password !== "") {
            auth.register(route, form, formType);
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
      .get("/google-auth/link")
      .then((res) => {
        window.location.href = res.data.url;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const fields = [];
  if (route === "/enterprises/register") {
    fields.push(
      {
        id: "name",
        label: "Name",
        type: "text",
        placeholder: "Name",
        onChange: (e) => setName(e.target.value),
      },
      {
        id: "owner",
        label: "Owner",
        type: "text",
        placeholder: "Owner",
        onChange: (e) => setOwner(e.target.value),
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "Email",
        onChange: (e) => setEmail(e.target.value),
      },
      {
        id: "password",
        label: "Password",
        type: "password",
        placeholder: "********",
        onChange: (e) => setPassword(e.target.value),
      },
      {
        id: "avatar",
        label: "Avatar",
        type: "file",
        onChange: (e) => setAvatar(e.target.files[0]),
      }
    );
  } else if (route === "/enterprises/login") {
    fields.push(
      {
        id: "username",
        label: "Email",
        type: "text",
        placeholder: "Email",
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
  } else if (route === "/users/register") {
    fields.push(
      {
        id: "username",
        label: "Username",
        type: "text",
        placeholder: "Username",
        onChange: (e) => setUsername(e.target.value),
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "Email",
        onChange: (e) => setEmail(e.target.value),
      },
      {
        id: "password",
        label: "Password",
        type: "password",
        placeholder: "********",
        onChange: (e) => setPassword(e.target.value),
      },
      {
        id: "avatar",
        label: "Avatar",
        type: "file",
        onChange: (e) => setAvatar(e.target.files[0]),
      }
    );
  } else {
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
  }

  if (googleId) {
    fields.push(
      {
        id: "username",
        label: "Username",
        type: "text",
        placeholder: "Username",
        onChange: (e) => setUsername(e.target.value),
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "Email",
        value: email,
        disabled: true,
      }
    );
  }

  return (
    <AuthForm
      fields={fields}
      handleSubmit={handleSubmit}
      formType={formType}
      methodType={methodType}
      setFormType={setFormType}
      googleAuth={googleAuth}
    />
  );
}

export default HandleForm;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";


function PasswordChange() {
  const [oldPswd, setOldPswd] = useState("");
  const [newPswd, setNewPswd] = useState("");
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload on form submission
    const data = {
      old_password: oldPswd,
      new_password: newPswd,
    };
  
    try {
      const res = await api.put("/settings/password", data);
      if (res.status === 202) {
        console.log("Password updated");
        navigate("/");
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="m-5">
      <form className="w-full max-w-lg" onSubmit={handleSubmit}>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700
              text-xs font-bold mb-2"
              htmlFor="grid-old-pswd"
            >
              Old password:
            </label>
            <input
              onChange={(e) => setOldPswd(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
              border-gray-200 rounded py-3 px-4 leading-tight 
              focus:outline-none focus:bg-white focus:border-gray-500"
              id="grid-old-pswd"
              type="password"
              placeholder="********"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide 
              text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-new-pswd"
            >
              New password:
            </label>
            <input
              onChange={(e) => setNewPswd(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 leading-tight 
                focus:outline-none focus:bg-white focus:border-gray-500"
              id="grid-new-pswd"
              type="password"
              placeholder="********"
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
  );
}

export default PasswordChange;

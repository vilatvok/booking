import { useNavigate } from "react-router-dom";
import api from "../utils/api";


function Settings() {
  const navigate = useNavigate();
  const deleteUser = async () => {
    await api.delete("/users/me").
      then((res) => {
        if (res.status === 204) {
          localStorage.clear();
          navigate("/auth/login");
        }
      }).
      catch((err) => {
        console.log(err);
      });
  }

  return (
    <div className="m-5">
      <button
        onClick={() => deleteUser()}
        className="inline-flex items-center px-3 py-2 text-sm font-medium 
        text-center text-white bg-teal-500
        rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
        focus:ring-blue-300 dark:bg-teal-500
        dark:hover:bg-teal-600 dark:focus:ring-blue-800"
      >
        Deactivate
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
  );
}


export default Settings;
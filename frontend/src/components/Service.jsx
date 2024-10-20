import api from "../utils/api";
import { useEffect, useState } from "react";
import { useCurrentObj } from "../hooks/useCurrentObject";

function Service({ service, onDelete, onUpdate }) {
  const [description, setDescription] = useState("");
  const [editing, setEditing] = useState(false);
  const username = useCurrentObj().name;
  const owner_model = service.owner_model;
  const owner = service.owner;
  const profileUrl = owner_model === "User" ? `/users/${owner}` : `/enterprises/${owner}`;

  useEffect(() => {
    setDescription(service.description);
  }, [service]);

  const image = "http://localhost:8000/" + service.images[0]?.data;

  const updateService = (event, id) => {
    event.preventDefault();
    api
      .patch(`/services/${id}`, { description })
      .then((res) => {
        if (res.status === 202) {
          console.log("updated");
          setEditing(false);
        } else {
          console.log("error");
        }
        onUpdate(username);
      })
      .catch((err) => console.log(err));
  };

  const deleteService = (id) => {
    api
      .delete(`/services/${id}`)
      .then((res) => {
        if (res.status === 204) {
          console.log("deleted");
        } else {
          console.log("error");
        }
        onDelete(username);
      })
      .catch((err) => console.log(err));
  };

  return (
    <>
      <a href="#!">
        <img className="rounded-t-lg" src={image} alt="Los Angeles Skyscrapers" />
      </a>
      <div className="p-6 bg-gray-900">
        <h5 className="mb-2 text-xl font-bold leading-tight">
          <a href={profileUrl}>
            {owner}
          </a>
        </h5>
        <p className="mb-4 text-base">{service.description}</p>
        <a
          href="#"
          onClick={() => setEditing(!editing)}
          className="inline-flex items-center px-3 py-2 text-sm font-medium 
        text-center text-white bg-teal-500 rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
        focus:ring-blue-300 dark:bg-teal-500 dark:hover:bg-teal-600 dark:focus:ring-blue-800"
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
        </a>
        <a
          href="#"
          onClick={() => deleteService(service.id)}
          className="inline-flex items-center px-3 py-2 ms-2 text-sm font-medium 
        text-center text-white bg-teal-500 rounded-lg hover:bg-teal-600 focus:ring-4 focus:outline-none 
        focus:ring-blue-300 dark:bg-teal-500 dark:hover:bg-teal-600 dark:focus:ring-blue-800"
        >
          Delete
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
        </a>
        {editing && (
          <form className="max-w-sm mx-auto">
            <div className="mb-2 mt-2">
              <label
                htmlFor="avatar"
                className="block mb-2 text-sm font-medium text-gray-900"
              >
                Description
              </label>
              <input
                type="description"
                id="description"
                className="bg-gray-50 border border-gray-300 
              text-gray-900 text-sm rounded-lg 
              focus:ring-blue-500 focus:border-blue-500 block w-full 
              p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 
              dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <button
              onClick={(e) => updateService(e, service.id)}
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
    </>
  );
}

export default Service;

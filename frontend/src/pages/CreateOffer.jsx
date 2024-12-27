import api from "../utils/api";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CreateOffer() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState("apartment");
  const [city, setCity] = useState("kyiv");
  const [phone, setPhone] = useState("");
  const [PricePerHour, setPricePerHour] = useState("");
  const [PricePerDay, setPricePerDay] = useState("");
  const [PricePerMonth, setPricePerMonth] = useState("");
  const [PricePerYear, setPricePerYear] = useState("");
  const [images, setImages] = useState([]);

  const navigate = useNavigate();

  const createOffer = async (e) => {
    e.preventDefault();

    const form_data = new FormData();
    const offer = {
      name: name,
      description: description,
      offer_type: type,
      city: city,
      phone: phone,
      images: images,
      prices: {
        per_hour: PricePerHour,
        per_day: PricePerDay,
        per_month: PricePerMonth,
        per_year: PricePerYear,
      },
    };

    form_data.append("form_data", JSON.stringify(offer));
    for (let i = 0; i < images.length; i++) {
      form_data.append("images", images[i]);
    }

    try {
      const res = await api.post("/offers", form_data);
      console.log(res.data);
      navigate("/"); // Navigate to the main page after successful creation
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="m-5">
      <form className="w-full max-w-lg" onSubmit={createOffer}>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700
              text-xs font-bold mb-2"
              htmlFor="grid-name"
            >
              Name
            </label>
            <input
              onChange={(e) => setName(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
              border-gray-200 rounded py-3 px-4 leading-tight 
              focus:outline-none focus:bg-white focus:border-gray-500"
              id="grid-name"
              type="text"
              placeholder="Loco"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide 
              text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-descr"
            >
              Description
            </label>
            <input
              onChange={(e) => setDescription(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 leading-tight 
                focus:outline-none focus:bg-white focus:border-gray-500"
              id="grid-descr"
              type="text"
              placeholder="This offer..."
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-type"
            >
              Type
            </label>
            <div className="relative">
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="block appearance-none w-full bg-gray-200 border border-gray-200 
                text-gray-700 py-3 px-4 pr-8 rounded leading-tight 
                focus:outline-none focus:bg-white focus:border-gray-500"
                id="grid-type"
              >
                <option>hotel</option>
                <option>apartment</option>
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
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-phone"
            >
              Phone
            </label>
            <input
              onChange={(e) => setPhone(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-phone"
              type="text"
              placeholder="097..."
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-city"
            >
              City
            </label>
            <div className="relative">
              <select
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="block appearance-none w-full bg-gray-200 border border-gray-200 
                text-gray-700 py-3 px-4 pr-8 rounded leading-tight 
                focus:outline-none focus:bg-white focus:border-gray-500"
                id="grid-state"
              >
                <option>kyiv</option>
                <option>lviv</option>
                <option>odessa</option>
              </select>
              <div
                className="pointer-events-none absolute inset-y-0 
                right-0 flex items-center px-2 text-gray-700"
              >
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
        <div className="flex flex-wrap -mx-3 mb-2">
          <div className="w-full md:w-1/4 px-3 mb-6 md:mb-0">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-per-hour"
            >
              per hour
            </label>
            <input
              onChange={(e) => setPricePerHour(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-per-hour"
              type="text"
              placeholder="23"
            />
          </div>
          <div className="w-full md:w-1/4 px-3 mb-6 md:mb-0">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-per-day"
            >
              per day
            </label>
            <input
              onChange={(e) => setPricePerDay(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-per-day"
              type="text"
              placeholder="23"
            />
          </div>
          <div className="w-full md:w-1/4 px-3 mb-6 md:mb-0">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-per-month"
            >
              per month
            </label>
            <input
              onChange={(e) => setPricePerMonth(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-per-month"
              type="text"
              placeholder="23"
            />
          </div>
          <div className="w-full md:w-1/4 px-3 mb-6 md:mb-0">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-per-year"
            >
              per year
            </label>
            <input
              onChange={(e) => setPricePerYear(e.target.value)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-per-year"
              type="text"
              placeholder="23"
            />
          </div>
        </div>
        <div className="flex flex-wrap -mx-3 mb-6">
          <div className="w-full px-3">
            <label
              className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
              htmlFor="grid-images"
            >
              Images
            </label>
            <input
              onChange={(e) => setImages(e.target.files)}
              className="appearance-none block w-full bg-gray-200 text-gray-700 border 
                border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none 
                focus:bg-white focus:border-gray-500"
              id="grid-images"
              type="file"
              multiple
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
              Create
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default CreateOffer;

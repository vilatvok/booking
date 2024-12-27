import api from "../utils/api";
import User from "../components/User";
import Company from "../components/Company";
import Offer from "../components/Offer";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";


function UserOffers({ currUser }) {
  const [user, setUser] = useState([]);
  const [offers, setOffers] = useState([]);
  const username = currUser;

  useEffect(() => {
    getUser(username);
    getOffers(username);
  }, [username]);

  const getUser = async (username) => {
    await api
      .get(`/users/${username}`)
      .then((res) => res.data)
      .then((data) => setUser(data))
      .catch((err) => console.log(err));
  };

  const getOffers = async (username) => {
    await api
      .get(`/users/${username}/offers`)
      .then((res) => res.data)
      .then((data) => setOffers(data))
      .catch((err) => console.log(err));
  };

  const listOffers = offers.map((item) => {
    return (
      <div
        className="mx-3 mt-6 flex flex-col rounded-lg bg-white 
        text-surface shadow-secondary-1 
        dark:bg-surface-dark dark:text-white 
        sm:shrink-0 sm:grow sm:basis-0"
        key={item.id}
      >
        <Offer
          offer={item}
          onDelete={(u) => getOffers(u)}
          onUpdate={(u) => getOffers(u)}
        />
      </div>
    );
  });

  return (
    <div className="m-5">
      <User user={user} onUpdate={(u) => getUser(u)} />
      <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
        {listOffers}
      </div>
    </div>
  );
}


function CompanyOffers({ currEnter }) {
  const [company, setCompany] = useState([]);
  const [offers, setOffers] = useState([]);
  const username = currEnter;

  useEffect(() => {
    getCompany(username);
    getOffers(username);
  }, [username]);

  const getCompany = async (name) => {
    await api
      .get(`/companies/${name}`)
      .then((res) => res.data)
      .then((data) => setCompany(data))
      .catch((err) => console.log(err));
  };

  const getOffers = async (name) => {
    await api
      .get(`/companies/${name}/offers`)
      .then((res) => res.data)
      .then((data) => setOffers(data))
      .catch((err) => console.log(err));
  };

  const listOffers = offers.map((item) => {
    return (
      <div
        className="mx-3 mt-6 flex flex-col rounded-lg bg-white 
        text-surface shadow-secondary-1 
        dark:bg-surface-dark dark:text-white 
        sm:shrink-0 sm:grow sm:basis-0"
        key={item.id}
      >
        <Offer
          offer={item}
          onDelete={(u) => getOffers(u)}
          onUpdate={(u) => getOffers(u)}
        />
      </div>
    );
  });
  return (
    <>
      <div className="m-5">
        <Company
          company={company}
          onUpdate={(u) => getCompany(u)}
        />
        <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
          {listOffers}
        </div>
      </div>
    </>
  );
}

function Profile() {
  const { name } = useParams();
  const url = window.location.href.includes("users");

  return (
    <div>
      {url && (
        <UserOffers currUser={name} />
      )}
      {!url &&
        <CompanyOffers currEnter={name} />
      }
    </div>
  );
}

export default Profile;

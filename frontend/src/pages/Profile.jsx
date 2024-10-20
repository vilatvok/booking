import api from "../utils/api";
import User from "../components/User";
import Enterprise from "../components/Enterprise";
import Service from "../components/Service";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";


function UserService({ currUser }) {
  const [user, setUser] = useState([]);
  const [services, setServices] = useState([]);
  const objName = currUser;

  useEffect(() => {
    getUser(objName);
    getServices(objName);
  }, [objName]);

  const getUser = async (username) => {
    await api
      .get(`/users/${username}`)
      .then((res) => res.data)
      .then((data) => setUser(data))
      .catch((err) => console.log(err));
  };

  const getServices = async (username) => {
    await api
      .get(`/users/${username}/services`)
      .then((res) => res.data)
      .then((data) => setServices(data))
      .catch((err) => console.log(err));
  };

  const listServices = services.map((item) => {
    return (
      <div
        className="mx-3 mt-6 flex flex-col rounded-lg bg-white 
        text-surface shadow-secondary-1 
        dark:bg-surface-dark dark:text-white 
        sm:shrink-0 sm:grow sm:basis-0"
        key={item.id}
      >
        <Service
          service={item}
          onDelete={(u) => getServices(u)}
          onUpdate={(u) => getServices(u)}
        />
      </div>
    );
  });

  return (
    <div className="m-5">
      <User user={user} onUpdate={(u) => getUser(u)} />
      <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
        {listServices}
      </div>
    </div>
  );
}

function EnterpriseService({ currEnter }) {
  const [enterprise, setEnterprise] = useState([]);
  const [services, setServices] = useState([]);
  const objName = currEnter;

  useEffect(() => {
    getEnterprise(objName);
    getServices(objName);
  }, [objName]);

  const getEnterprise = async (name) => {
    await api
      .get(`/enterprises/${name}`)
      .then((res) => res.data)
      .then((data) => setEnterprise(data))
      .catch((err) => console.log(err));
  };

  const getServices = async (name) => {
    await api
      .get(`/enterprises/${name}/services`)
      .then((res) => res.data)
      .then((data) => setServices(data))
      .catch((err) => console.log(err));
  };

  const listServices = services.map((item) => {
    return (
      <div
        className="mx-3 mt-6 flex flex-col rounded-lg bg-white 
        text-surface shadow-secondary-1 
        dark:bg-surface-dark dark:text-white 
        sm:shrink-0 sm:grow sm:basis-0"
        key={item.id}
      >
        <Service
          service={item}
          onDelete={(u) => getServices(u)}
          onUpdate={(u) => getServices(u)}
        />
      </div>
    );
  });
  return (
    <>
      <div className="m-5">
        <Enterprise
          enterprise={enterprise}
          onUpdate={(u) => getEnterprise(u)}
        />
        <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
          {listServices}
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
        <UserService currUser={name} />
      )}
      {!url &&
        <EnterpriseService currEnter={name} />
      }
    </div>
  );
}

export default Profile;

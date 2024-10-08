import api from "../utils/api"
import User from "../components/User"
import Service from "../components/Service";
import { useEffect, useState } from "react"
import { useCurrentObj } from '../hooks/useCurrentObject';


function UserService() {
  const [user, setUser] = useState([]);
  const [services, setServices] = useState([]);
  const objName = useCurrentObj().name;


  useEffect(() => {
    getUser(objName)
    getServices(objName)
  }, [objName])

  const getUser = (username) => {
    api.get(`/users/${username}`)
      .then((res) => res.data)
      .then((data) => setUser(data))
      .catch((err) => console.log(err))
  }

  const getServices = (username) => {
    api.get(`/users/${username}/services`)
      .then((res) => res.data)
      .then((data) => setServices(data))
      .catch((err) => console.log(err))
  }

  const listServices = services.map((item) => {
    return (
      <li key={item.id}>
        <Service
          service={item}
          onDelete={(u) => getServices(u)}
          onUpdate={(u) => getServices(u)}>
        </Service>
      </li>
    )
  })

  return (
    <>
      <div>
        <User user={user} onUpdate={(u) => getUser(u)}></User>
        {listServices}
      </div>
    </>
  )
}


function Home() {
  return (
    <>
      <div>
        <UserService />
      </div>
    </>
  )
}

export default Home
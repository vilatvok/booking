import { useState, useEffect } from 'react';
import api from '../utils/api';
import Service from '../components/Service';


function Home() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    getServices();
  }, [])

  const getServices = async () => {
    await api
      .get('/services')
      .then((res) => res.data)
      .then((data) => setServices(data))
      .catch((err) => console.error(err));
  }

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
    <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
      {listServices}
    </div>
  )
}

export default Home;

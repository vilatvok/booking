import { useState, useEffect } from 'react';
import api from '../utils/api';
import Offer from '../components/Offer';


function Home() {
  const [offers, setOffers] = useState([]);

  useEffect(() => {
    getOffers();
  }, [])

  const getOffers = async () => {
    await api
      .get('/offers')
      .then((res) => res.data)
      .then((data) => setOffers(data))
      .catch((err) => console.error(err));
  }

  const listOffers = offers.map((item) => {
    return (
      <div
        className="mx-3 mt-6 flex flex-col rounded-lg bg-white 
        text-surface shadow-secondary-1 
        dark:bg-surface-dark dark:text-white 
        sm:shrink-0 sm:grow sm:basis-0"
        key={item.id}
      >
        <Offer offer={item}/>
      </div>
    );
  });

  return (
    <div className="grid-cols-1 sm:grid md:grid-cols-3 ">
      {listOffers}
    </div>
  )
}

export default Home;

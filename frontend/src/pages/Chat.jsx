import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ACCESS_TOKEN } from '../data/constants';
import { useCurrentObj } from '../hooks/useCurrentObject';
import api from '../utils/api';


function Chat() {
  const { chat_id } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const currObjId = useCurrentObj().id;

  const token = localStorage.getItem(ACCESS_TOKEN);
  const websocket = new WebSocket(`ws://localhost:8000/chats/${chat_id}?token=${token}`);

  useEffect(() => {
    getMessages();
  }, [chat_id]);
  
  websocket.onmessage = (event) => {
    console.log(event.data)
    setMessages((prev) => [...prev, event.data]);
  };

  websocket.onopen = () => {
    console.log('WebSocket connected');
  };

  websocket.onclose = () => {
    console.log('WebSocket disconnected');
  };

  const getMessages = async () => {
    await api
      .get(`/chats/${chat_id}/messages`)
      .then((res) => res.data)
      .then((data) => setMessages(data))
      .catch((err) => console.log(err));
  }

  const sendMessage = () => {
    const data = {
      chat_id: chat_id,
      sender_id: currObjId,
      content: input,
    };
    websocket.send(JSON.stringify(data));
    setInput('');
  };

  return (
    <>
      <div className="flex flex-col items-center justify-center 
        w-screen min-h-screen bg-gray-100 text-gray-800 p-10">
        <div className="flex flex-col flex-grow 
          w-full max-w-xl bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="flex flex-col flex-grow h-0 p-4 overflow-auto">
            {messages.map((msg) => (
              msg.sender_id === currObjId ? (
                <div className="flex w-full mt-2 space-x-3 max-w-xs" key={msg.id}>
                  <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
                  <div>
                    <div className="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                      <p className="text-sm">{msg.content}</p>
                    </div>
                    <span className="text-xs text-gray-500 leading-none">2 min ago</span>
                  </div>
                </div>
              ) : (
                <div className="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end" key={msg.id}>
                  <div>
                    <div className="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                      <p className="text-sm">{msg.content}</p>
                    </div>
                    <span className="text-xs text-gray-500 leading-none">2 min ago</span>
                  </div>
                  <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
                </div>
              )
            ))}
          </div>
          <div className="bg-gray-300 p-4">
            <input className="flex items-center h-10 w-full rounded px-3 text-sm"
              type="text" placeholder="Type your message…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Chat;
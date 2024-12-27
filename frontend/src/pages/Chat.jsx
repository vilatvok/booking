import { useEffect, useState, useCallback, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { ACCESS_TOKEN } from '../data/constants';
import { useCurrentUser } from '../hooks/useCurrentUser';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import api from '../utils/api';

function Chat() {
  const { chat_id } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const currUserId = useCurrentUser().id;

  const socketUrl = useMemo(
    () => `ws://localhost:8000/chats/${chat_id}?token=${localStorage.getItem(ACCESS_TOKEN)}`,
    [chat_id]
  );

  const { readyState, sendMessage } = useWebSocket(socketUrl, {
    onOpen: () => console.log('WebSocket connected'),
    onMessage: (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev, message]);
    },
    onError: (error) => console.error('WebSocket error:', error),
    onClose: () => console.log('WebSocket disconnected'),
    shouldReconnect: () => true, // Automatically reconnect on disconnect
  });

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const { data } = await api.get(`/chats/${chat_id}/messages`);
        setMessages(data);
      } catch (error) {
        console.error('Failed to fetch messages:', error);
      }
    };
    fetchMessages();
  }, [chat_id]);

  const handleSendMessage = useCallback(() => {
    if (readyState === ReadyState.OPEN && input.trim()) {
      sendMessage(
        JSON.stringify({ chat_id, sender_id: currUserId, content: input })
      );
      setInput('');
    }
  }, [input, chat_id, currUserId, sendMessage, readyState]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSendMessage();
  };

  const connectionStatus = useMemo(() => {
    switch (readyState) {
      case ReadyState.CONNECTING:
        return 'Connecting...';
      case ReadyState.OPEN:
        return 'Connected';
      case ReadyState.CLOSING:
        return 'Disconnecting...';
      case ReadyState.CLOSED:
        return 'Disconnected';
      default:
        return 'Unknown';
    }
  }, [readyState]);

  return (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-gray-100 text-gray-800 p-10">
      <div className="flex flex-col flex-grow w-full max-w-xl bg-white shadow-xl rounded-lg overflow-hidden">
        <div className="flex justify-between items-center bg-gray-200 p-2">
          <h2 className="text-lg font-semibold">Chat Room</h2>
          <span className="text-xs text-gray-500">{connectionStatus}</span>
        </div>
        <div className="flex flex-col flex-grow h-0 p-4 overflow-auto">
          {messages.map((msg) => (
            <Message key={msg.id} message={msg} isCurrentUser={msg.sender_id === currUserId} />
          ))}
        </div>
        <div className="bg-gray-300 p-4 flex space-x-2">
          <input
            className="flex-1 h-10 rounded px-3 text-sm"
            type="text"
            placeholder="Type your message…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-600 text-white px-4 rounded"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const Message = ({ message, isCurrentUser }) => (
  <div
    className={`flex w-full mt-2 space-x-3 max-w-xs ${
      isCurrentUser ? 'ml-auto justify-end' : ''
    }`}
  >
    {!isCurrentUser && (
      <img
        className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"
        src={`http://localhost:8000/${message.sender.avatar}`}
        alt=""
      />
    )}
    <div>
      <span className="text-xs text-gray-500 leading-none">
        {message.sender.username}
      </span>
      <div
        className={`p-3 rounded-lg ${
          isCurrentUser
            ? 'bg-blue-600 text-white rounded-br-lg'
            : 'bg-gray-300 rounded-bl-lg'
        }`}
      >
        <p className="text-sm">{message.content}</p>
      </div>
      <span className="text-xs text-gray-500 leading-none">
        {message.timestamp}
      </span>
    </div>
    {isCurrentUser && (
      <img
        className="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"
        src={`http://localhost:8000/${message.sender.avatar}`}
        alt=""
      />
    )}
  </div>
);

export default Chat;

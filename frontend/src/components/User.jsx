import api from "../utils/api"
import { useState } from "react"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../data/constants";


function User({ user, onUpdate }) {
  const [username, setUsername] = useState(user.username);
  const [email, setEmail] = useState(user.email);
  const [avatar, setAvatar] = useState(user.avatar);
  const [editing, setEditing] = useState(false);

  // get tokens
  const accessToken = localStorage.getItem(ACCESS_TOKEN);
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);

  const refreshTokens = async () => {
    try {
      const res = await api.post('/users/token/refresh', {
        refresh: refreshToken,
        username: user.username
      }
      )
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        return res.status;
      }
    } catch (err) {
      console.log(err)
    }
    return;
  }

  const editUser = async () => {
    // generate form data
    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'multipart/form-data'
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('avatar', avatar);

    // send request
    await api
      .patch(`/users/${user.username}`, formData, headers)
      .then(async (res) => {
        if (res.status === 202) {
          console.log('Updated')
        } else {
          console.log('error')
        }
        // Update token data
        if (user.username !== username) {
          const response = await refreshTokens();
          if (response === 200) {
            onUpdate(username);
            setEditing(false);
          }
        }
      })
      .catch((err) => console.log(err.response))
  }

  return (
    <div className="max-w-sm w-full lg:max-w-full lg:flex m-5">
      <div
        className="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden"
        title="Woman holding a mug" style={{ backgroundImage: `url(http://localhost:8000/${user.avatar})` }}
      >
      </div>
      <div className="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t lg:border-gray-400 bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
        <div className="mb-8">
          <div className="text-gray-900 font-bold text-xl mb-2">
            {user.username}
          </div>
          <p className="text-gray-700 text-base">
            {user.email}
          </p>
        </div>
        <button onClick={() => setEditing(!editing)} className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Edit
          <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
          </svg>
        </button>
      {editing && (
        <form className="max-w-sm mx-auto">
          <div className="mb-2 mt-2">
            <label htmlFor="avatar" className="block mb-2 text-sm font-medium text-gray-900">Username</label>
            <input type="username" id="username" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@flowbite.com" value={username} onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div className="mb-2">
            <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900">Email</label>
            <input type="email" id="email" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" value={user.email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="mb-2">
            <label htmlFor="avatar" className="ms-2 text-sm font-medium text-gray-900">Avatar</label>
            <input id="avatar" type="file"
              onChange={(e) => setAvatar(e.target.files[0])} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
            
          </div>
          <button type="submit" onClick={editUser} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
        </form>
      )}
      </div>
    </div>

    //   style={{
    //     width: 300,
    //   }}
    //   actions={[
    //     <SettingOutlined key="setting" onClick={() => navigate("/create-service")}/>,
    //     <EditOutlined key="edit" onClick={() => setEditing(true)} />,
    //     <EllipsisOutlined key="ellipsis" />,
    //   ]}
    // >
    //   <Meta
    //     avatar={<Avatar src={ava} />}
    //     title={user.username}
    //     description={user.email}
    //   />
    //   {editing && (
    //     <div style={{ marginTop: 16 }}>
    //       <Input
    //         value={username}
    //         onChange={(e) => setUsername(e.target.value)}
    //         placeholder="Update username"
    //         />
    //       <Input
    //         value={email}
    //         onChange={(e) => setEmail(e.target.value)}
    //         placeholder="Update email"
    //         />
    //       <Button type="primary" onClick={editUser} style={{ marginTop: 8 }}>
    //         Update
    //       </Button>
    //     </div>
    //   )}
    // </Card>
  )
};


export default User

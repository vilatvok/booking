import api from '../utils/api';
import { ACCESS_TOKEN } from '../data/constants';
import { useState } from 'react';
import { useCurrentUser } from '../hooks/useCurrentUser';


function Service({ service, onDelete, onUpdate }) {
  const [description, setDescription] = useState(service.description);
  const [editing, setEditing] = useState(false);
  const username = useCurrentUser().username;

  const image = "http://localhost:8000/" + service.images[0]?.data
  const accessToken = localStorage.getItem(ACCESS_TOKEN);

  const deleteService = (id) => {
    api
      .delete(`/services/${id}`, {
        headers: {
          'Authorization': 'Bearer' + String(accessToken)
        }
      })
      .then((res) => {
        if (res.status === 204) {
          console.log('deleted');
        } else {
          console.log('error');
        };
        onDelete(username);
      })
      .catch((err) => console.log(err))
  }

  const updateService = (id) => {
    api.
      patch(`/services/${id}`, { description }, {
        headers: {
          'Authorization': 'Bearer' + String(accessToken)
        }
      })
      .then((res) => {
        if (res.status === 202) {
          console.log('updated')
          setEditing(false);
        } else {
          console.log('error');
        };
        onUpdate(username);
      })
      .catch((err) => console.log(err))
  }

  return (
    <div></div>
    // <Card
    //   style={{
    //     width: 300,
    //   }}
    //   cover={
    //     <img
    //       alt="example"
    //       src={image}
    //     />
    //   }
    //   actions={[
    //     <SettingOutlined key="setting" />,
    //     <EditOutlined key="edit" onClick={() => setEditing(true)} />,
    //     <EllipsisOutlined key="ellipsis" onClick={() => deleteService(service.id)} />,
    //   ]}
    // >
    //   <Meta
    //     avatar={<Avatar src="https://api.dicebear.com/7.x/miniavs/svg?seed=8" />}
    //     title={username}
    //     description={service.description}
    //   />
    //   {editing && (
    //     <div style={{ marginTop: 16 }}>
    //       <Input
    //         value={description}
    //         onChange={(e) => setDescription(e.target.value)}
    //         placeholder="Update description"
    //       />
    //       <Button type="primary" onClick={() => updateService(service.id)} style={{ marginTop: 8 }}>
    //         Update
    //       </Button>
    //     </div>
    //   )}
    // </Card>
  )
}


export default Service
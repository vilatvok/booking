import api from "../utils/api"
import { ACCESS_TOKEN } from "../data/constants"
import { useState } from "react"
import { useNavigate } from "react-router-dom";


function CreateService() {
  const accessToken = localStorage.getItem(ACCESS_TOKEN)
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState("");
  const [city, setCity] = useState("");
  const [phone, setPhone] = useState("");
  const [PricePerHour, setPricePerHour] = useState("");
  const [PricePerDay, setPricePerDay] = useState("");
  const [PricePerMonth, setPricePerMonth] = useState("");
  const [PricePerYear, setPricePerYear] = useState("");

  const [images, setImages] = useState([]);
  const navigate = useNavigate();

  const headers = {
    headers: {
      'Authorization': 'Bearer' + String(accessToken)
    }
  }

  const createService = (e) => {
    e.preventDefault();
    const form = new FormData();
    const service = {
      'name': name,
      'description': description,
      'type': type,
      'city': city,
      'phone': phone,
      'images': images,
      'prices': {
        'per_hour': PricePerHour,
        'per_day': PricePerDay,
        'per_month': PricePerMonth,
        'per_year': PricePerYear
      },
    }

    form.append('service', JSON.stringify(service))
    for (let i = 0; i < images.length; i++) {
      form.append('images', images[i]);
    }

    api.post("/services", form, headers).
      then((res) => console.log(res.data)).
      catch((err) => console.log(err));
    navigate("/", headers);
  }

  return (
    <div></div>
    // <Form
    //   variant="filled"
    //   onSubmitCapture={createService}
    //   style={{ maxWidth: 600 }}
    //   initialValues={{ variant: "filled" }}
    // >

    //   <Form.Item label="Name" name="Name" rules={[{ required: true, message: 'Please input!' }]}>
    //     <Input onChange={(e) => setName(e.target.value)} />
    //   </Form.Item>

    //   <Form.Item
    //     label="Description"
    //     name="Description"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <Input.TextArea onChange={(e) => setDescription(e.target.value)} />
    //   </Form.Item>

    //   <Form.Item
    //     label="Phone"
    //     name="Phone"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <Input onChange={(e) => setPhone(e.target.value)} />
    //   </Form.Item>

    //   <Form.Item
    //     label="Type"
    //     name="Type"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <Select onChange={(e) => setType(e)}>
    //       <Select.Option value="hotel">Hotel</Select.Option>
    //       <Select.Option value="apartment">Apartment</Select.Option>
    //     </Select>
    //   </Form.Item>

    //   <Form.Item
    //     label="City"
    //     name="City"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <Select onChange={(e) => setCity(e)}>
    //       <Select.Option value="lviv">Lviv</Select.Option>
    //       <Select.Option value="kyiv">Kyiv</Select.Option>
    //     </Select>
    //   </Form.Item>
    //   <Form.Item
    //     label="Price per hour"
    //     name="PricePerHour"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <InputNumber onChange={(e) => setPricePerHour(e)} style={{ width: '100%' }} />
    //   </Form.Item>
    //   <Form.Item
    //     label="Price per day"
    //     name="PricePerDay"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <InputNumber onChange={(e) => setPricePerDay(e)} style={{ width: '100%' }} />
    //   </Form.Item>
    //   <Form.Item
    //     label="Price per month"
    //     name="PricePerMonth"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <InputNumber onChange={(e) => setPricePerMonth(e)} style={{ width: '100%' }} />
    //   </Form.Item>
    //   <Form.Item
    //     label="Price per year"
    //     name="PricePerYear"
    //     rules={[{ required: true, message: 'Please input!' }]}
    //   >
    //     <InputNumber onChange={(e) => setPricePerYear(e)} style={{ width: '100%' }} />
    //   </Form.Item>

    //   <input type="file" onChange={(e) => setImages(e.target.files)} multiple accept=".jpg, .jpeg, .png" />

    //   <Form.Item wrapperCol={{ offset: 6, span: 16 }}>
    //     <Button type="primary" htmlType="submit">
    //       Create
    //     </Button>
    //   </Form.Item>
    // </Form>
  );
};


export default CreateService
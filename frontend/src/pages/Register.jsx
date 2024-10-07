import HandleForm from "../components/Form"

import { useLocation } from "react-router-dom"


function Register() {
		const location = useLocation();
		if (location.state) {
			return (
				<HandleForm 
					route="/google-auth/register" 
					method="register" 
					googleData={location.state.googleData}>
				</HandleForm>
			)
		} else {
			return (
				<HandleForm 
					route="/users/register" 
					method="register" 
					googleData={null}>
				</HandleForm>
			)
		}
}

export default Register
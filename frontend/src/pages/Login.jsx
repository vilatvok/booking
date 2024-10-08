import HandleForm from "../components/AuthForm"


export function UserLogin() {
    return <HandleForm route="/users/login" method="login"/>
}

export function EnterpriseLogin() {
    return <HandleForm route="/enterprises/login" method="login" />
}

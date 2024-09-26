import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../data/constants";


export function useCurrentUser() {
  const token = localStorage.getItem(ACCESS_TOKEN)
  const decoded = jwtDecode(token);
  return decoded;
}

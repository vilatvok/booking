import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../data/constants";


export function useCurrentObj() {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (!token) {
    return null;
  }
  const decoded = jwtDecode(token);
  return decoded;
}

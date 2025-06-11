// src/axiosInstance.js
import axios from "axios";

// axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api/",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// 요청 보내기 전에 로컬스토리지에서 access token을 읽어서 Authorization에 추가
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    } else {
      delete config.headers["Authorization"];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;

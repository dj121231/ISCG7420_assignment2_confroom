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

// 응답 인터셉터: 401(만료)시 토큰 자동 갱신 및 재시도
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // 무한루프 방지: 이미 재시도한 요청은 skip
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem("refresh")
    ) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh");
        const res = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          { refresh: refreshToken },
          { headers: { "Content-Type": "application/json" } }
        );
        const newAccess = res.data.access;
        localStorage.setItem("access", newAccess);
        // Authorization 헤더 갱신
        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // refresh 실패: 로그아웃 처리
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/"; // 또는 로그인 페이지로 리다이렉트
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

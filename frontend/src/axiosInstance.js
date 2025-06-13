// src/axiosInstance.js - Configures axios with JWT authentication for API requests
import axios from "axios";

// Create an axios instance with base URL for the backend API
const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

// Add a request interceptor to attach JWT access token to every request
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("access");
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to handle token refresh on 401 errors
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // If 401 error and not already retried, try to refresh token
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh");
        if (refreshToken) {
          const response = await axios.post(
            process.env.REACT_APP_API_URL + "/token/refresh/",
            { refresh: refreshToken },
            { headers: { "Content-Type": "application/json" } }
          );
          localStorage.setItem("access", response.data.access);
          axiosInstance.defaults.headers["Authorization"] =
            "Bearer " + response.data.access;
          originalRequest.headers["Authorization"] =
            "Bearer " + response.data.access;
          return axiosInstance(originalRequest);
        }
      } catch (err) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

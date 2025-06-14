import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await axios.post("http://localhost:8000/api/token/", {
        username: formData.username,
        password: formData.password,
      });
      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      navigate("/");
      window.location.reload();
    } catch (err) {
      setError("Invalid username or password.");
    }
  };

  return (
    <div
      className="card-section small-card"
      style={{ maxWidth: "400px", margin: "0 auto" }}
    >
      <div className="card-title">Login</div>
      {error && (
        <div
          style={{
            color: "#c62828",
            fontSize: "0.95rem",
            marginBottom: "12px",
          }}
        >
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} style={{ fontSize: "0.95rem" }}>
        <div className="input-row">
          <label className="label" htmlFor="username">
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="input"
            required
            placeholder="Enter your username"
          />
        </div>
        <div className="input-row">
          <label className="label" htmlFor="password">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="input"
            required
            placeholder="Enter your password"
          />
        </div>
        <div className="btn-group">
          <button type="submit" className="btn btn-primary">
            Login
          </button>
        </div>
        <div
          style={{ marginTop: "16px", textAlign: "center", fontSize: "0.9rem" }}
        >
          Don't have an account?{" "}
          <a
            href="/signup"
            style={{ color: "#1976d2", textDecoration: "none" }}
          >
            Sign Up
          </a>
        </div>
      </form>
    </div>
  );
};

export default Login;

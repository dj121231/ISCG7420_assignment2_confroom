import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "",
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

    if (formData.password !== formData.password2) {
      setError("Passwords don't match");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/api/register/", {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.password2,
      });

      // After successful registration, log the user in
      const loginResponse = await axios.post(
        "http://localhost:8000/api/token/",
        {
          username: formData.username,
          password: formData.password,
        }
      );

      localStorage.setItem("access", loginResponse.data.access);
      localStorage.setItem("refresh", loginResponse.data.refresh);
      navigate("/");
      window.location.reload(); // Reload to update user context
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.password ||
          "Registration failed. Please try again."
      );
    }
  };

  return (
    <div
      className="card-section small-card"
      style={{ maxWidth: "400px", margin: "0 auto" }}
    >
      <div className="card-title">Sign Up</div>
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
            placeholder="Choose a username"
          />
        </div>
        <div className="input-row">
          <label className="label" htmlFor="email">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="input"
            required
            placeholder="Enter your email"
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
            placeholder="Choose a password"
          />
        </div>
        <div className="input-row">
          <label className="label" htmlFor="password2">
            Confirm Password
          </label>
          <input
            type="password"
            id="password2"
            name="password2"
            value={formData.password2}
            onChange={handleChange}
            className="input"
            required
            placeholder="Confirm your password"
          />
        </div>
        <div className="btn-group">
          <button type="submit" className="btn btn-primary">
            Sign Up
          </button>
        </div>
        <div
          style={{ marginTop: "16px", textAlign: "center", fontSize: "0.9rem" }}
        >
          Already have an account?{" "}
          <a href="/login" style={{ color: "#1976d2", textDecoration: "none" }}>
            Login
          </a>
        </div>
      </form>
    </div>
  );
};

export default Signup;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "",
    role: "user",
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
      await axios.post("http://localhost:8000/api/register/", {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password2: formData.password2,
        role: formData.role,
      });

      // Try to log in the user automatically after successful registration
      try {
        const loginResponse = await axios.post(
          "http://localhost:8000/api/token/",
          {
            username: formData.username,
            password: formData.password,
          }
        );
        if (
          loginResponse.data &&
          loginResponse.data.access &&
          loginResponse.data.refresh
        ) {
          localStorage.setItem("access", loginResponse.data.access);
          localStorage.setItem("refresh", loginResponse.data.refresh);
          navigate("/");
          window.location.reload(); // Reload to update user context
        } else {
          setError(
            "Registration succeeded, but auto-login failed. Please log in manually."
          );
        }
      } catch (loginErr) {
        setError(
          "Registration succeeded, but auto-login failed. Please log in manually."
        );
      }
    } catch (err) {
      // Collect all error messages from backend and display them
      let errorMsg = "Registration failed. Please try again.";
      if (err.response && err.response.data) {
        if (typeof err.response.data === "string") {
          errorMsg = err.response.data;
        } else if (typeof err.response.data === "object") {
          errorMsg = Object.values(err.response.data).flat().join(" ");
        }
      }
      setError(errorMsg);
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
            wordBreak: "break-all",
            whiteSpace: "pre-line",
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
        <div className="input-row">
          <label className="label" htmlFor="role">
            Role
          </label>
          <select
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            className="input"
            required
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
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

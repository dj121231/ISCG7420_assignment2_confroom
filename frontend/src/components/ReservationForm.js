import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";

const ReservationForm = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    room: "",
    date: "",
    start_time: "",
    end_time: "",
  });

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axiosInstance.get("/rooms/");
        console.log("Fetched rooms:", response.data);
        setRooms(response.data);
      } catch (err) {
        console.error("Room fetch error:", err);
        setError("Failed to load rooms.");
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
  }, []);

  // Generate 30-min interval options from 09:00 to 18:00
  const timeOptions = [];
  for (let h = 9; h <= 18; h++) {
    for (let m of [0, 30]) {
      if (h === 18 && m > 0) continue;
      const timeStr = `${h.toString().padStart(2, "0")}:${
        m === 0 ? "00" : "30"
      }:00`;
      timeOptions.push(timeStr);
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const newValue = name === "room" ? parseInt(value) || "" : value;
      console.log(`Updating ${name}:`, {
        value,
        newValue,
        type: typeof newValue,
      });
      return { ...prev, [name]: newValue };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Create payload with explicit room ID conversion
    const payload = {
      ...formData,
      room: parseInt(formData.room),
    };

    // Log form data and verify room type before submission
    console.log("Form data before submission:", {
      ...formData,
      roomType: typeof formData.room,
      roomValue: formData.room,
    });
    console.log("Payload with explicit room conversion:", {
      ...payload,
      roomType: typeof payload.room,
      roomValue: payload.room,
    });

    try {
      const response = await axiosInstance.post("/reservations/", payload);
      console.log("Reservation response:", response.data);
      setSuccess("Reservation created successfully!");
      setFormData({
        title: "",
        room: "",
        date: "",
        start_time: "",
        end_time: "",
      });
    } catch (err) {
      console.error("Reservation error:", err.response?.data);
      let errMsg = "An error occurred.";
      if (err.response && err.response.data) {
        errMsg = JSON.stringify(err.response.data);
      }
      setError(errMsg);
    }
  };

  if (loading)
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>Loading rooms...</div>
    );

  return (
    <div>
      <div className="card-title">Create Reservation</div>
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
      {success && (
        <div
          style={{
            color: "#1b7f2a",
            fontSize: "0.95rem",
            marginBottom: "12px",
          }}
        >
          {success}
        </div>
      )}
      <form onSubmit={handleSubmit} style={{ fontSize: "0.95rem" }}>
        <div className="input-row">
          <label className="label" htmlFor="title">
            Title
          </label>
          <input
            className="input"
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="Enter reservation title"
          />
        </div>
        <div className="input-row">
          <label className="label" htmlFor="room">
            Room
          </label>
          <select
            className="input"
            id="room"
            name="room"
            value={formData.room}
            onChange={handleChange}
            required
          >
            <option value="">Select a room</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name} • {room.location} • {room.capacity} seats
              </option>
            ))}
          </select>
        </div>
        <div className="input-row">
          <label className="label" htmlFor="date">
            Date
          </label>
          <input
            className="input"
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        <div style={{ display: "flex", gap: "12px" }}>
          <div className="input-row" style={{ flex: 1 }}>
            <label className="label" htmlFor="start_time">
              Start Time
            </label>
            <select
              className="input"
              id="start_time"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              required
            >
              <option value="">Select start time</option>
              {timeOptions.map((time) => (
                <option key={time} value={time}>
                  {time.slice(0, 5)}
                </option>
              ))}
            </select>
          </div>
          <div className="input-row" style={{ flex: 1 }}>
            <label className="label" htmlFor="end_time">
              End Time
            </label>
            <select
              className="input"
              id="end_time"
              name="end_time"
              value={formData.end_time}
              onChange={handleChange}
              required
            >
              <option value="">Select end time</option>
              {timeOptions.map((time) => (
                <option key={time} value={time}>
                  {time.slice(0, 5)}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="btn-group">
          <button className="btn btn-primary" type="submit">
            Create Reservation
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReservationForm;

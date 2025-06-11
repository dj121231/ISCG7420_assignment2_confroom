import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosInstance";

const ReservationForm = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [formData, setFormData] = useState({
    room: "",
    date: "",
    start_time: "",
    end_time: "",
  });

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axiosInstance.get("/rooms/");
        setRooms(response.data);
      } catch (err) {
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
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      await axiosInstance.post("/reservations/", formData);
      setSuccess("Reservation created successfully!");
      setFormData({ room: "", date: "", start_time: "", end_time: "" });
    } catch (err) {
      let errMsg = "An error occurred.";
      if (err.response && err.response.data) {
        errMsg = JSON.stringify(err.response.data);
      }
      setError(errMsg);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Create Reservation</h1>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {success && <div style={{ color: "green" }}>{success}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Room:</label>
          <select
            name="room"
            value={formData.room}
            onChange={handleChange}
            required
          >
            <option value="">-- Select a room --</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name} (Location: {room.location}, Capacity:{" "}
                {room.capacity})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Date:</label>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Start Time:</label>
          <select
            name="start_time"
            value={formData.start_time}
            onChange={handleChange}
            required
          >
            <option value="">-- Select start time --</option>
            {timeOptions.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>End Time:</label>
          <select
            name="end_time"
            value={formData.end_time}
            onChange={handleChange}
            required
          >
            <option value="">-- Select end time --</option>
            {timeOptions.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ReservationForm;

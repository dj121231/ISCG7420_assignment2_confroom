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

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Create Reservation</h1>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {success && <div style={{ color: "green" }}>{success}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            style={{ marginBottom: "10px", width: "100%", padding: "5px" }}
          />
        </div>
        <div>
          <label>Room:</label>
          <select
            name="room"
            value={formData.room}
            onChange={handleChange}
            required
          >
            <option value="">-- Select a room --</option>
            {rooms.map((room) => {
              console.log(`Creating option for room:`, room);
              return (
                <option key={room.id} value={room.id}>
                  {room.name} (Location: {room.location}, Capacity:{" "}
                  {room.capacity})
                </option>
              );
            })}
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

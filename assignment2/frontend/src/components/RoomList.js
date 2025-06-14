// RoomList.js - Displays a list of all available conference rooms
import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const RoomList = () => {
  // State for rooms, loading, and error
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch room list on mount
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

  if (loading)
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>Loading rooms...</div>
    );
  if (error)
    return <div style={{ color: "#c62828", fontSize: "0.95rem" }}>{error}</div>;
  if (rooms.length === 0)
    return <div style={{ fontSize: "0.95rem" }}>No rooms available.</div>;

  // Render the list of rooms
  return (
    <div>
      <div className="card-title">Room List</div>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {rooms.map((room) => (
          <li
            key={room.id}
            style={{
              marginBottom: "12px",
              padding: "8px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          >
            <div>
              <strong>{room.name}</strong> ({room.location})
            </div>
            <div>Capacity: {room.capacity} seats</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomList;

import React, { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";

const RoomList = () => {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axiosInstance.get("/rooms/");
        setRooms(response.data);
      } catch (error) {
        console.error("Error fetching rooms:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
  }, []);

  if (loading) {
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>Loading rooms…</div>
    );
  }

  if (rooms.length === 0) {
    return (
      <div style={{ fontSize: "0.95rem", color: "#666" }}>
        No rooms available.
      </div>
    );
  }

  return (
    <div>
      <div className="card-title">Room List</div>
      <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
        {rooms.map((room) => (
          <li
            key={room.id}
            style={{
              padding: "10px 0",
              borderBottom: "1px solid #e3e8ef",
              fontSize: "0.95rem",
            }}
          >
            <div
              style={{
                fontWeight: "bold",
                color: "#1976d2",
                marginBottom: "4px",
              }}
            >
              {room.name}
            </div>
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "8px 16px",
                color: "#555",
              }}
            >
              <span>
                <strong style={{ color: "#666" }}>Location:</strong>{" "}
                {room.location}
              </span>
              <span>
                <strong style={{ color: "#666" }}>Capacity:</strong>{" "}
                {room.capacity}
              </span>
              <span>
                <strong style={{ color: "#666" }}>Status:</strong>
                <span
                  style={{
                    color: room.is_active ? "#1b7f2a" : "#c62828",
                    marginLeft: "4px",
                  }}
                >
                  {room.is_active ? "Active" : "Inactive"}
                </span>
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomList;

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
    return <div>Loading…</div>;
  }

  if (rooms.length === 0) {
    return <div>No rooms available.</div>;
  }

  return (
    <div>
      <h1>Room List</h1>
      <ul>
        {rooms.map((room) => (
          <li key={room.id}>
            <strong>Name:</strong> {room.name} <br />
            <strong>Location:</strong> {room.location} <br />
            <strong>Capacity:</strong> {room.capacity} <br />
            <strong>Status:</strong> {room.is_active ? "Active" : "Inactive"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RoomList;

import React from "react";

const CurrentUserInfo = ({ user }) => {
  // If user prop is not passed, fallback to localStorage or context (for demo)
  // You can adjust this logic as needed.
  return (
    <div
      style={{
        display: "flex",
        gap: "24px",
        alignItems: "center",
        fontSize: "0.95rem",
      }}
    >
      <div style={{ fontWeight: "bold", color: "#1976d2" }}>Current User:</div>
      <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
        <span>
          <strong>Username:</strong> {user?.username || "kimdongju"}
        </span>
        <span>
          <strong>Email:</strong> {user?.email || ""}
        </span>
        <span>
          <strong>Role:</strong> {user?.is_staff ? "Admin" : "User"}
        </span>
      </div>
    </div>
  );
};

export default CurrentUserInfo;

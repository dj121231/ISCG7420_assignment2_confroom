import React from "react";

const CurrentUserInfo = ({ user }) => {
  if (!user) {
    return (
      <div style={{ fontWeight: "bold", color: "#c62828" }}>Not logged in</div>
    );
  }
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
          <strong>Username:</strong> {user.username}
        </span>
        <span>
          <strong>Email:</strong> {user.email}
        </span>
        <span>
          <strong>Role:</strong> {user.is_staff ? "Admin" : "User"}
        </span>
      </div>
    </div>
  );
};

export default CurrentUserInfo;

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link as RouterLink } from "react-router-dom";
import { TextField, Button, Typography, Card, CardContent, Box } from "@mui/material";

axios.defaults.withCredentials = true;
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await axios.post(`${API_URL}/register`, { email, password });
      setSuccess(res.data.message); // show success message
      setTimeout(() => navigate("/login"), 1500); // navigate after short delay
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed.");
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f4f6f8">
      <Card sx={{ width: 400, borderRadius: 3, boxShadow: 6 }}>
        <CardContent>
          <Typography variant="h5" align="center" gutterBottom color="primary">
            Register
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Email"
              type="email"
              fullWidth
              margin="normal"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <TextField
              label="Password (Min 6 characters)"
              type="password"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && (
              <Typography color="error" align="center" sx={{ mt: 1 }}>
                {error}
              </Typography>
            )}
            {success && (
              <Typography color="success.main" align="center" sx={{ mt: 1 }}>
                {success}
              </Typography>
            )}
            <Button type="submit" variant="contained" fullWidth sx={{ mt: 2, py: 1.2 }}>
              Register
            </Button>
          </form>
          <Typography variant="body2" align="center" sx={{ mt: 2, color: "text.secondary" }}>
            Already have an account?{" "}
            <Button
              component={RouterLink}
              to="/login"
              variant="text"
              size="small"
              sx={{
                textTransform: "none",
                fontWeight: "bold",
                color: "#1976d2",
                ml: 0.5,
                p: 0,
                minWidth: 0,
              }}
            >
              Login
            </Button>
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Register;

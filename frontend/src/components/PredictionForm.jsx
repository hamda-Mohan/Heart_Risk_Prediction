import React, { useState } from "react";
import axios from "axios";
import { Snackbar, Alert } from "@mui/material";
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Divider,
  Grid,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Tooltip,
} from "@mui/material";
import { Logout, Favorite, Warning, CheckCircle } from "@mui/icons-material";
import Confetti from "react-confetti";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";


axios.defaults.withCredentials = true;
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const initialInput = {
  Age: 0,
  Chest_Pain: 0,
  Shortness_of_Breath: 0,
  Fatigue: 0,
  Palpitations: 0,
  Dizziness: 0,
  Swelling: 0,
  Pain_Arms_Jaw_Back: 0,
  Cold_Sweats_Nausea: 0,
  High_BP: 0,
  High_Cholesterol: 0,
  Diabetes: 0,
  Smoking: 0,
  Obesity: 0,
  Sedentary_Lifestyle: 0,
  Family_History: 0,
  Chronic_Stress: 0,
};

const symptomTips = {
  Chest_Pain: "Pain or discomfort in the chest area",
  Shortness_of_Breath: "Difficulty breathing during activity",
  Fatigue: "Feeling unusually tired",
  Palpitations: "Noticeable rapid heartbeat",
  Dizziness: "Feeling lightheaded or faint",
  Swelling: "Swelling in legs, feet, or ankles",
  Pain_Arms_Jaw_Back: "Pain radiating to arms, jaw, or back",
  Cold_Sweats_Nausea: "Cold sweats or nausea episodes",
  High_BP: "High blood pressure",
  High_Cholesterol: "High cholesterol levels",
  Diabetes: "History of diabetes",
  Smoking: "Currently smoking",
  Obesity: "Overweight or obesity",
  Sedentary_Lifestyle: "Lack of regular physical activity",
  Family_History: "Family history of heart disease",
  Chronic_Stress: "Long-term stress",
};

const PredictionForm = () => {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();
  const [input, setInput] = useState(initialInput);
  const [age, setAge] = useState("");
  const [model, setModel] = useState("rf");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: "", severity: "info" });


  const handleSwitch = (e) => {
    const { name, checked } = e.target;
    setInput((prev) => ({ ...prev, [name]: checked ? 1 : 0 }));
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleReset = () => {
    setAge("");
    setInput(initialInput);
    setResult(null);
    setOpenDialog(false);
  };

 const handleSubmit = async (e) => {
  e.preventDefault();

  if (!user) {
    setSnackbar({ open: true, message: "Please login to access the prediction feature.", severity: "warning" });
    return;
  }
  if (age === "" || age < 20 || age > 100) {
    setSnackbar({ open: true, message: "Please enter a valid age between 20 and 100.", severity: "error" });
    return;
  }

  try {
    setLoading(true);
    const res = await axios.post(
      `${API_URL}/predict?model=${model}`,
      { ...input, Age: Number(age) },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setResult(res.data);
    setOpenDialog(true);
  } catch (err) {
    setSnackbar({ open: true, message: "Prediction failed. Please check backend connection.", severity: "error" });
    console.error(err);
  } finally {
    setLoading(false);
  }
};


  const handleCloseDialog = () => setOpenDialog(false);

  const riskColor = result?.prediction === 1 ? "error.main" : "success.main";
  const RiskIcon = result?.prediction === 1 ? Warning : CheckCircle;

  return (
    <Box>
      {/* AppBar */}
      <AppBar
        position="static"
        sx={{
          background: "linear-gradient(90deg, #2196F3, #21CBF3)",
          mb: 4,
        }}
      >
        <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
          <Box display="flex" alignItems="center">
            <Favorite sx={{ mr: 1 }} />
            <Typography variant="h6">Heart Risk Predictor</Typography>
          </Box>
          {user && (
            <IconButton color="inherit" onClick={handleLogout}>
              <Logout />
            </IconButton>
          )}
        </Toolbar>
      </AppBar>

      {/* Prediction Form */}
      <Box display="flex" justifyContent="center" px={1}>
        <Card sx={{ width: "90%", maxWidth: 700, borderRadius: 3, boxShadow: 6 }}>
          <CardContent>
            <Typography variant="h5" align="center" gutterBottom color="primary">
              Heart Disease Prediction
            </Typography>

            <form onSubmit={handleSubmit}>
              <TextField
                label="Age"
                type="number"
                fullWidth
                value={age}
                onChange={(e) => setAge(e.target.value)}
                sx={{ mb: 1 }}
                required
                inputProps={{ min: 20, max: 100 }}
                error={age !== "" && (age < 20 || age > 100)}
                helperText={age !== "" && (age < 20 || age > 100) ? "Age must be between 20 and 100" : ""}
              />

              <Divider sx={{ mb: 1 }} />

              <Grid container spacing={1}>
                {Object.keys(initialInput)
                  .filter((key) => key !== "Age")
                  .map((symptom) => (
                    <Grid size={{ xs: 8, sm: 4}} key={symptom}>
                      <Tooltip title={symptomTips[symptom] || ""} arrow>
                        <FormControlLabel
                          control={
                            <Switch
                              checked={input[symptom] === 1}
                              onChange={handleSwitch}
                              name={symptom}
                              color={input[symptom] === 1 ? "error" : "success"}
                            />
                          }
                          label={symptom.replaceAll("_", " ")}
                        />
                      </Tooltip>
                    </Grid>
                  ))}
              </Grid>

              <Divider sx={{ my: 3 }} />

              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography>Model:</Typography>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  style={{
                    padding: "8px 12px",
                    borderRadius: "8px",
                    border: "1px solid #ccc",
                  }}
                >
                  <option value="rf">Random Forest</option>
                  <option value="lr">Logistic Regression</option>
                  <option value="xgb">XGBoost</option>
                </select>
              </Box>

              <Box display="flex" gap={2}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  disabled={loading}
                  sx={{ py: 1.5, fontWeight: "bold" }}
                >
                  {loading ? "Predicting..." : "Predict Risk"}
                </Button>
                <Button
                  type="button"
                  variant="outlined"
                  color="secondary"
                  fullWidth
                  sx={{ py: 1.5 }}
                  onClick={handleReset}
                >
                  Reset
                </Button>
              </Box>
            </form>
          </CardContent>
        </Card>
      </Box>

      {/* Result Dialog */}
      {result && (
        <Dialog
          open={openDialog}
          onClose={handleCloseDialog}
          PaperProps={{
            sx: { borderRadius: 3, minWidth: 300, p: 2, textAlign: "center" },
          }}
        >
          {!result.prediction && <Confetti width={window.innerWidth} height={window.innerHeight} />}
          <DialogTitle>
            <Box display="flex" alignItems="center" color={riskColor} justifyContent="center">
              <RiskIcon sx={{ mr: 1 }} />
              {result.prediction === 1 ? "High Risk Detected" : "Low Risk Detected"}
            </Box>
          </DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Probability:
            </Typography>
            <LinearProgress
              variant="determinate"
              value={Math.round(result.probability * 100)}
              sx={{
                height: 10,
                borderRadius: 5,
                mb: 2,
                backgroundColor: "#eee",
                "& .MuiLinearProgress-bar": {
                  backgroundColor: result.prediction === 1 ? "#f44336" : "#4caf50",
                },
              }}
            />
            <Typography variant="body2">
              {Math.round(result.probability * 100)}%
            </Typography>
            <Divider sx={{ my: 1 }} />
            <Typography variant="caption" color="text.secondary">
              Model Used: {result.model}
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="primary" variant="contained">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      )}
      {/* ---------------- CONFETTI FOR LOW RISK ---------------- */}
      {result?.prediction === 0 && <Confetti recycle={false} numberOfPieces={200} />}
      {/* ---------------- SNACKBAR FOR MESSAGES ---------------- */}
      <Snackbar
  open={snackbar.open}
  autoHideDuration={4000}
  onClose={() => setSnackbar({ ...snackbar, open: false })}
  anchorOrigin={{ vertical: "top", horizontal: "center" }}
>
  <Alert
    onClose={() => setSnackbar({ ...snackbar, open: false })}
    severity={snackbar.severity}
    variant="filled"
    sx={{ width: "100%" }}
  >
    {snackbar.message}
  </Alert>
</Snackbar> 
    </Box>
  );
  
  
};

export default PredictionForm;

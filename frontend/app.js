const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const API_URL = process.env.API_URL || "http://api:8000";
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`, {}, { timeout: 5000 });
    res.json(response.data);
  } catch (err) {
    console.error(`Submit error: ${err.message}`);
    res.status(500).json({ error: "Failed to submit job. Please try again." });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`, { timeout: 5000 });
    res.json(response.data);
  } catch (err) {
    console.error(`Status error: ${err.message}`);
    res.status(500).json({ error: "Failed to get job status. Please try again." });
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});

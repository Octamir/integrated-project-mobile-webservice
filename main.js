"use strict";

const port = 3000;

const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());

app.get('/', (req, res) => res.send('Test'));

app.listen(port, () => console.log(`Listening on port ${port}`));

"use strict";

const port = 3000;

const express = require('express');
const cors = require('cors');
const axios = require('axios');

const robot = 'http://192.168.56.101:5000/';

const app = express();
app.use(cors());

app.get('/', (req, res) => res.send('Test'));

app.get('/get-name', (req, res) => {
    axios.get(robot + 'getName')
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        });
});

app.get('/get-type', (req, res) => {
    axios.get(robot + 'getType')
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        });
});

app.get('/get-battery', (req, res) => {
    axios.get(robot + 'getBatteryLevel')
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        });
});

app.get('/actions/stand-init', (req, res) => {
    axios.get(robot + 'actions/StandInit')
        .then((data) => {
            console.log('StandInit');
            res.send(data.data);
        });
});

app.get('/actions/sit-relax', (req, res) => {
    axios.get(robot + 'actions/SitRelax')
        .then((data) => {
            console.log('SitRelax');
            res.send(data.data);
        });
});

app.get('/actions/stand-zero', (req, res) => {
    axios.get(robot + 'actions/StandZero')
        .then((data) => {
            console.log('StandZero');
            res.send(data.data);
        });
});

app.get('/actions/lying-belly', (req, res) => {
    axios.get(robot + 'actions/LyingBelly')
        .then((data) => {
            console.log('LyingBelly');
            res.send(data.data);
        });
});

app.get('/actions/lying-back', (req, res) => {
    axios.get(robot + 'actions/LyingBack')
        .then((data) => {
            console.log('LyingBack');
            res.send(data.data);
        });
});

app.get('/actions/stand', (req, res) => {
    axios.get(robot + 'actions/Stand')
        .then((data) => {
            console.log('Stand');
            res.send(data.data);
        });
});

app.get('/actions/crouch', (req, res) => {
    axios.get(robot + 'actions/Crouch')
        .then((data) => {
            console.log('Crouch');
            res.send(data.data);
        });
});

app.get('/actions/sit', (req, res) => {
    axios.get(robot + 'actions/Sit')
        .then((data) => {
            console.log('Sit');
            res.send(data.data);
        });
});

app.listen(port, () => console.log(`Listening on port ${port}`));

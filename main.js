"use strict";

const port = 3000;

const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());

const errorHandler = (res, err) => {
    // Right now we'll only handle the robot not being found
    // If more errors need to be handled, err's code should be checked
    res.status(503).send('Robot cannot be accessed')
};

app.get('/', (req, res) => res.send('Test'));

app.get('/:ip/get-name', (req, res) => {
    axios.get(`http://${req.params.ip}/getName`)
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/get-type', (req, res) => {
    axios.get(`http://${req.params.ip}/getType`)
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/get-battery', (req, res) => {
    axios.get(`http://${req.params.ip}/getBatteryLevel`)
        .then((data) => {
            console.log(data.data);
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/stand-init', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/StandInit`)
        .then((data) => {
            console.log('StandInit');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/sit-relax', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/SitRelax`)
        .then((data) => {
            console.log('SitRelax');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/stand-zero', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/StandZero`)
        .then((data) => {
            console.log('StandZero');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/lying-belly', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/LyingBelly`)
        .then((data) => {
            console.log('LyingBelly');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/lying-back', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/LyingBack`)
        .then((data) => {
            console.log('LyingBack');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/stand', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/Stand`)
        .then((data) => {
            console.log('Stand');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/crouch', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/Crouch`)
        .then((data) => {
            console.log('Crouch');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/sit', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/Sit`)
        .then((data) => {
            console.log('Sit');
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/ask/:text', (req,res) => {
    axios.get(`http://${req.params.ip}/ask/${req.params.text}`)
        .then((data) => {
        console.log(`${req.params.text}`)
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/move/:x/:y/:d', (req,res) => {
    axios.get(`http://${req.params.ip}/move/${req.params.x}/${req.params.y}/${req.params.d}`)
        .then((data) => {
            console.log(`x:${req.params.x}y:${req.params.y}d:${req.params.d}`)
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.listen(port, () => console.log(`Listening on port ${port}`));

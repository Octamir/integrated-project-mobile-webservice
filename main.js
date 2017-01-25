"use strict";

const port = 3000;

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const axios = require('axios');

const app = express()
    .use(cors())
    .use(morgan('dev'));

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

app.get('/:ip/get-actions', (req, res) => {
    axios.get(`http://${req.params.ip}/getActions`)
        .then((data) => res.send(data.data))
        .catch((err) => errorHandler(res, err));
});

app.get('/:ip/actions/:action', (req, res) => {
    axios.get(`http://${req.params.ip}/actions/${req.params.action}`)
        .then((data) => res.send(data.data))
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

app.get('/:ip/get-picture', (req,res) => {
    axios.get(`http://${req.params.ip}/getPicture`)
        .then((data) => {
            res.send(data.data);
        })
        .catch((err) => errorHandler(res, err));
});

app.listen(port, () => console.log(`Listening on port ${port}`));

//server/index.js

const express = require('express');
const logger = require('morgan');
const cors = require('cors');
const { spawn } = require("child_process")

const PORT = process.env.PORT || 3001;

const app = express();

app.use(cors({
    origin: 'http://localhost:3000',
    credentials: true
}));
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

//let jsonArray = [];

let python = false;


const portData = async () => {
    return new Promise((resolve, reject) => {
        python.stdout.once('data', resolve)
        python.stdout.once('error', reject)

    })
}

app.post('/apiSetProcessInstance', async (req, res) => {
    if (python) {
        console.log("Process Restarting...")
        python.kill('SIGINT')
    }
    console.log("Process Started.")
    python = spawn('python3', ['-u', 'scheduler.py']);

    const sendInstance = {
        cars: req.body.state.cars,
        intersection: req.body.state.intersection
    };
    python.stdin.write(JSON.stringify(sendInstance) + '\n');
    res.send(await portData())
})

app.get('/apiUpdateTick', async (req, res) => {
    console.log("Updating Tick...")
    const sendUpdateSignal = {};
    python.stdin.write(JSON.stringify(sendUpdateSignal) + '\n');
    res.send(await portData())
})

app.listen(PORT, () => {
    console.log(`Server Listening on ${PORT}`);
});
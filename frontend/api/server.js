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

python = false;

const portData = async () => {
    return new Promise((resolve) => {
        python.stdout.once('data', resolve)
    })
}

const initializeProcess = (process) => {
    if (python) {
        console.log("Process Restarting...")
        python.kill('SIGINT')
    }
    console.log("Process Started.")
    python = spawn('python3', ['-u', 'scheduler.py']);
}

app.post('/apiSetProcessInstance', (req, res) => {
    initializeProcess(python);

    const sendInstance = req.body;
    python.stdin.write(JSON.stringify(sendInstance) + '\n');

    portData()
        .then((updatedTick) => res.send(updatedTick));
})

app.post('/apiUpdateTick', (req, res) => {
    const sendUpdateSignal = req.body;
    python.stdin.write(JSON.stringify(sendUpdateSignal) + '\n');

    portData()
        .then((updatedTick) => res.send(updatedTick))
})

app.listen(PORT, () => {
    console.log(`Server Listening on ${PORT}`);
});
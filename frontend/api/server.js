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

let jsonArray = [];

const python = spawn('python3', ['-u', 'scheduler.py']);
python.stdout.on('data', (data) => {
    console.log("Python_Process Output:", data.toString())
    jsonArray.push(data.toString())
})

const portData = async () => {
    return new Promise((resolve, reject) => {
        python.stdout.once('data', resolve)
        python.stdout.once('error', reject)

    })
}

app.post('/apiStartProcess', async (req, res) => {
    console.log("Json received for transfer");
    const jsonOut = {
        cars: req.body.state.cars,
        intersection: req.body.state.intersection
    };
    console.log(jsonOut);
    python.stdin.write(JSON.stringify(jsonOut) + '\n');
    console.log("json", jsonArray)
    res.send(await portData())
})


app.post('/apiPauseState', (req, res) => {
    /*
    console.log("Pause state received for transfer");
    const jsonOut = {
        pause: req.body.state.pause
    }
    python.stdin.write(JSON.stringify(jsonOut) + '\n');
    console.log("json", jsonArray);
    res.send(jsonArray);
    */
})

app.post('/apiRestartState', (req, res) => {
    python.on("close", function () {
        // Wait for process to exit, then run again

        python = spawn('python3', ['-u', 'scheduler.py']);
    });
})


app.listen(PORT, () => {
    console.log(`Server Listening on ${PORT}`);
});
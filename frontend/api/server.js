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

/* PortData
    Reads python child process std out and returns a promise for output data.
    In any instance where the python output would be rejected .on('error', reject) 
    the python process is restarted instead.*/
const portData = async () => {
    return new Promise((resolve) => {
        python.stdout.once('data', resolve)
    })
}

/* initializeProcess
    Takes in the spawn syscall and initializes the python process.
    If the python process is already initialized, it restarts the Process.*/
const initializeProcess = (process) => {
    if (python) {
        console.log("Process Restarting...")
        python.kill('SIGINT')
    }
    console.log("Process Started.")
    python = spawn('python3', ['-u', 'scheduler.py']);
}
/* apiCall setProcessInstance
    Initializes the python process with all criticalState values: intersectionType, and algorithmValue.
    Outputs stdout as a JSON for React to read. */
app.post('/apiSetProcessInstance', (req, res) => {
    initializeProcess(python);

    const sendInstance = req.body;
    python.stdin.write(JSON.stringify(sendInstance) + '\n');

    portData()
        .then((updatedTick) => res.send(updatedTick));
})

/* apiCall updateTick
    Updates an initialized process with any continuousState changes,
    and receives updated car positions as a JSON, with statistics and traffic light data */
app.post('/apiUpdateTick', (req, res) => {
    const sendUpdateSignal = req.body;
    python.stdin.write(JSON.stringify(sendUpdateSignal) + '\n');

    portData()
        .then((updatedTick) => res.send(updatedTick))
})

app.listen(PORT, () => {
    console.log(`Server Listening on ${PORT}`);
});
import axios from 'axios';

/* Calls the api with intersection state and returns the first child_process tick */
function setProcessInstance(state) {
    return axios
        .post('http://localhost:3001/apiSetProcessInstance', state)
        .then((output) => { return output.data })
}

/* Calls the api to return the next child_process tick */
function updateTick(state) {
    return axios
        .post('http://localhost:3001/apiUpdateTick', state)
        .then((output) => { return output.data })
}

/* Takes in any api function (apiCall) and updates any useState hook (setState) with the values returned from api */
const updateState = (apiCall, state, setState) => {
    apiCall(state).then((returnState) => {
        setState(returnState)
    })
}

export { updateState, updateTick, setProcessInstance }
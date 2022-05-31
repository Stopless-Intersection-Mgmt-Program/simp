import '../css/App.css';
import { useState, useEffect } from 'react';
import World from './appComponents/world.js';
import { layoutMappings } from './appComponents/worldComponents/intersection.js'
import { updateState, updateTick, setProcessInstance } from './appComponents/apiCalls'
import DropDown from './appComponents/dropdown.js';
import Button from './appComponents/button.js'
import Typography from '@mui/material/Typography';
import Slider from '@mui/material/Slider'

const App = () => {

  /* UseState Hooks
      Forces a rerender of associated components when
      state variables change. */

  const [btnActive, setBtnActive] = useState(false);
  const [intersectionValue, setIntersectionValue] = useState('4-Way Intersection');
  const [algorithmValue, setAlgorithmValue] = useState('First Come First Served');
  const [speedLimit, setSpeedLimit] = useState(30);
  const [playSpeed, setPlaySpeed] = useState(4);
  const [bufferValue, setBufferValue] = useState(0);
  const [spawnRate, setSpawnRate] = useState(1.5);
  const [returnState, setReturnState] = useState({ cars: [] });

  /* Handles state for critical variables
      algorithmValue: The algorithm to be used
      layout: the intersection to be used*/
  let criticalState = {
    once:
    {
      algorithm: algorithmValue,
      layout: layoutMappings[intersectionValue]
    },
    continuous:
    {
      playSpeed: playSpeed,
      spawnRate: spawnRate,
      speedLimit: speedLimit,
      buffer: bufferValue
    }
  }
  /* Spawns python3 child process with initialized intersection values
    Using the setProcessInstance api call. Updates returnState  */
  useEffect(() => {
    updateState(setProcessInstance, criticalState, setReturnState)
  }, [intersectionValue, algorithmValue])

  /* Updates python3 child process on a 20ms interval to receive updated car positions.
    Uses updateTick apicall, and updates returnState */
  useEffect(() => {
    //Handles Continuous State for real-time variable changes
    let continuousState = {
      continuous:
      {
        playSpeed: playSpeed,
        spawnRate: spawnRate,
        speedLimit: speedLimit,
        buffer: bufferValue
      }
    }
    const interval = setInterval(() => {
      if (btnActive) updateState(updateTick, continuousState, setReturnState);
    }, 20);
    return () => clearInterval(interval);
  }, [bufferValue, playSpeed, spawnRate, speedLimit, btnActive]);

  return (
    <>
      <div className="pageRow">
        <div className="pageColumn">
          {/* Title */}
          <div style={{ textAlign: 'center', paddingTop: "1%", width: "100%", height: '17.5vh' }}>
            <h1 style={{ color: '#80959B' }}>Stopless Intersection Management Program</h1>
            <h2 style={{ color: '#406168' }}>(SIMP)</h2>
          </div>
          {/* World 
              Relative positioning environment for road, lane, and car components
              Given three types:
              worldWidth, worldHeight, and
              intersectionType: the intersection type to be rendered
              algorithmType: */}
          <World
            worldWidth={600}
            worldHeight={600}
            intersectionType={intersectionValue}
            btnActive={btnActive}
            returnState={returnState} />
        </div>
        {/* SettingsWrapper 
            Holds dropdown, sliders, and buttons*/}
        <div className='settingsWrapper'>
          {/* DropDown Components */}
          <DropDown
            name='Algorithm:'
            default="First Come First Served"
            setValueForParent={setAlgorithmValue}
            options={['First Come First Served', 'Traffic Light']} />

          <DropDown
            name='Intersection:'
            default="4-Way Intersection"
            setValueForParent={setIntersectionValue}
            options={['4-Way Intersection', 'T-Way Intersection', 'T-Way Flipped']} />
          {/* End of DropDown Components */}

          {/* Slider Components */}
          <Typography htmlFor='SpawnRate'>Spawn Rate: {spawnRate}</Typography>
          <Slider
            id='SpawnRate'
            size='large'
            value={spawnRate}
            min={0}
            max={5}
            step={0.1}
            width="20%"
            onChange={(event) => setSpawnRate(parseInt(event.target.value))}></Slider>

          <Typography id='SpeedLimit'>Speed Limit: {speedLimit}</Typography>
          <Slider
            id='SpeedLimit'
            size='large'
            value={speedLimit}
            min={1}
            max={30}
            step={1}
            width="20%"
            onChange={(event) => setSpeedLimit(parseInt(event.target.value))}></Slider>

          <Typography id='Buffer' align='left'>Buffer: {bufferValue}</Typography>
          <Slider
            size='large'
            value={bufferValue}
            min={0}
            max={4}
            step={0.1}
            width="20%"
            onChange={(event) => setBufferValue(parseInt(event.target.value))}></Slider>

          <Typography id='PlaySpeed'>Play Speed: {playSpeed}</Typography>
          <Slider
            id='PlaySpeed'
            size='large'
            value={playSpeed}
            min={0}
            max={10}
            step={1}
            width="20%"
            onChange={(event) => setPlaySpeed(parseInt(event.target.value))}></Slider>
          {/* End of Slider components */}
          <div style={{ display: "flex", flexDirection: "row", width: "100%" }}>
            {/* Play Button */}
            <Button func={setBtnActive} arg={btnActive} name={btnActive ? "Pause" : "Begin"} />
            {/* Restart Button */}
            <Button func={updateState} arg={[setProcessInstance, criticalState, setReturnState]} name={"Restart"} />
          </div>
        </div>
      </div>
    </>
  )
}

export default App;

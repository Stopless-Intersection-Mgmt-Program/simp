import '../css/App.css';
import { useState, useEffect } from 'react';
import DropDown from './appComponents/dropdown.js';
import Button from './appComponents/button.js'
import World from './appComponents/world.js';
import { layoutMappings } from './appComponents/worldComponents/intersection.js'
import { updateState, updateTick, setProcessInstance } from './appComponents/apiCalls'

const App = () => {
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
  const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
  const intersectionLength = vw * .396825

  /* UseState Hooks
      Forces a rerender of associated components when
      state variables change. */

  const [numCars, setNumCars] = useState(5);
  const [btnActive, setBtnActive] = useState(false);
  const [situationValue, setSituationValue] = useState('Any');
  const [intersectionValue, setIntersectionValue] = useState('4-Way Intersection');
  const [algorithmValue, setAlgorithmValue] = useState('First Come First Served');
  const [speedLimit, setSpeedLimit] = useState(30);
  const [playSpeed, setPlaySpeed] = useState(2);
  const [bufferValue, setBufferValue] = useState(0);
  const [spawnRate, setSpawnRate] = useState(1.5);

  let criticalState = {
    once:
    {
      algorithmValue: algorithmValue,
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

  let continuousState = {
    continuous:
    {
      playSpeed: playSpeed,
      spawnRate: spawnRate,
      speedLimit: speedLimit,
      buffer: bufferValue
    }
  }

  const [returnState, setReturnState] = useState({ cars: [] });

  /* Spawns python3 child process with initialized intersection values
    Using the setProcessInstance api call. Updates returnState  */
  useEffect(() => {
    updateState(setProcessInstance, criticalState, setReturnState)
  }, [intersectionValue, situationValue, algorithmValue])

  /* Updates python3 child process on a 10ms interval to receive updated car positions.
    Uses updateTick apicall, and updates returnState */
  useEffect(() => {
    const interval = setInterval(() => {
      if (btnActive) { updateState(updateTick, continuousState, setReturnState) }
    }, 20);
    return () => clearInterval(interval);
  }, [returnState, btnActive]);


  return (
    <>
      {/* Title */}
      <div style={{ textAlign: 'center', paddingTop: "1%" }}>
        <h1 style={{ color: '#80959B' }}>Stopless Intersection Management Program</h1>
        <h2 style={{ color: '#406168' }}>(SIMP)</h2>
      </div>
      {/* worldComponent 
            Renders road, lane, and car components
            Given three types:
              worldWidth, worldHeight, and
              intersectiontype: the intersection type to be rendered */}
      <World
        worldWidth={600}
        worldHeight={600}
        vh={vh}
        vw={vw}
        intersectionType={intersectionValue}
        algorithmType={algorithmValue}
        numCars={numCars}
        btnActive={btnActive}
        returnState={returnState} />

      {/* SettingsWrapper 
            Holds the dropdownComponent,
              * Must be attached with a label *

              if state is to be tracked use situationValue, setSituationValue to 
              retrieve user selected input events with a useState hook.
              
              Given an array of 'options' component populates the dropdown menu.*/}

      <div className='settingsWrapper'>

        <DropDown
          name='Algorithm:'
          setValueForParent={setAlgorithmValue}
          options={['First Come First Served', 'Traffic Light', 'Priority Scheduling', 'Round Robin', '... Add More']} />

        <DropDown
          name='Intersection:'
          setValueForParent={setIntersectionValue}
          options={['4-Way Intersection', 'T-Way Intersection', 'X-Way Intersection', 'Multi-Way Intersection', '... Add More']} />

        <DropDown
          name='Situation:'
          setValueForParent={setSituationValue}
          options={['Any', '3-Car Staggered', '3-Car Simultaneous', '... Add More']} />

        <label htmlFor='SpawnRate'>Spawn Rate: {spawnRate}</label>
        <input
          id='SpawnRate'
          type='range'
          min='0'
          max='5'
          step='.1'
          value={spawnRate}
          onInput={(inputEvent) => setSpawnRate(inputEvent.target.value)} />

        <label htmlFor='SpeedLimit'>Speed Limit: {speedLimit}</label>
        <input
          id='SpeedLimit'
          type='range'
          min='0'
          max='30'
          step='1'
          value={speedLimit}
          onInput={(inputEvent) => setSpeedLimit(inputEvent.target.value)} />

        <label htmlFor='Buffer'>Buffer: {bufferValue}</label>
        <input
          id='Buffer'
          type='range'
          min='0'
          max='2'
          step='.1'
          value={bufferValue}
          onInput={(inputEvent) => setBufferValue(inputEvent.target.value)} />

        <label htmlFor='PlaySpeed'>Play Speed: {playSpeed}</label>
        <input
          id='PlaySpeed'
          type='range'
          min='1'
          max='10'
          step='1'
          value={playSpeed}
          onInput={(inputEvent) => setPlaySpeed(inputEvent.target.value)} />


        {/* Play Button */}
        <Button func={setBtnActive} arg={btnActive} name={btnActive ? "Pause" : "Begin"} />
        {/* Restart Button */}
        <Button func={updateState} arg={[setProcessInstance, criticalState, setReturnState]} name={"Restart"} />
      </div>
    </>
  )
}

export default App;

import '../css/App.css';
import { useState } from 'react';
import DropDown from './dropdown';
import { World, layoutMappings } from './worldComponents';
import axios from 'axios';

function stateToJSON(state) {
  console.log("JSON transfer started with,", state)

  axios
    .post('http://localhost:3001/apiStartProcess', state)
    .then((output) => console.log("JSON transferred to express:", output))

}

function pauseState(bool) {
  console.log("Pause state initiated with bool", bool)
  let pauseState = { state: { pause: bool } }
  axios
    .post('http://localhost:3001/apiPauseState', pauseState)
    .then(() => console.log("Pause state sent"))
}

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

  const [criticalState, setCriticalState] = useState({
    state:
    {
      cars: ['NULL'],
      intersection: [intersectionLength, layoutMappings[intersectionValue], algorithmValue, situationValue] //waiting for algorithmType to be saved currently 0
    }
  })

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
        intersectionType={intersectionValue}
        algorithmType={algorithmValue} />

      {/* SettingsWrapper 
            Holds the dropdownComponent,
              * Must be attached with a label *

              if state is to be tracked use situationValue, setSituationValue to 
              retrieve user selected input events with a useState hook.
              
              Given an array of 'options' component populates the dropdown menu.*/}

      <div className='settingsWrapper'>

        <label htmlFor='algorithm'>Algorithm:</label>
        <DropDown
          id='algorithm'
          setValueForParent={setAlgorithmValue}
          options={['First Come First Served', 'Shortest Job Next', 'Priority Scheduling', 'Round Robin', '... Add More']} />

        <label htmlFor='intersection'>Intersection:</label>
        <DropDown
          id='intersection'
          setValueForParent={setIntersectionValue}
          options={['4-Way Intersection', 'T-Way Intersection', 'X-Way Intersection', 'Multi-Way Intersection', '... Add More']} />

        <label htmlFor='situation'>Situation:</label>

        <DropDown
          id='situation'
          setValueForParent={setSituationValue}
          options={['Any', '3-Car Staggered', '3-Car Simultaneous', '... Add More']} />

        {situationValue === 'Any' ?
          <>
            {/* Slider for populating cars */}
            <label htmlFor='totalCars'>Total Cars: {numCars}</label>
            <input
              id='totalCars'
              type='range'
              min='0'
              max='32'
              step='1'
              value={numCars}
              onInput={(inputEvent) => setNumCars(inputEvent.target.value)} />
          </>
          :
          null}

        {/* Play Button */}
        <div
          id='btn'
          className='btn'
          width="100%"
          onClick={(event) => { setBtnActive(!btnActive); btnActive ? pauseState(btnActive) : stateToJSON(criticalState) }}>
          {btnActive ? "Pause" : "Begin"}
        </div>
      </div>
    </>
  )
}

export default App;

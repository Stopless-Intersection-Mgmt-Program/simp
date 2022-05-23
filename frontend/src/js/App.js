import '../css/App.css';
import { useState, useEffect } from 'react';
import DropDown from './dropdown';
import World from './worldComponents';
import { layoutMappings } from './intersection'
import axios from 'axios';


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
  const [carArray, setCarArray] = useState([]);
  let criticalState = {
    state:
    {
      cars: carArray,
      intersection: [93, layoutMappings[intersectionValue], algorithmValue, situationValue]
    }
  }

  const [returnState, setReturnState] = useState();

  function stateToJSON(state) {
    console.log("JSON transfer started with,", state)
    axios
      .post('http://localhost:3001/apiStartProcess', state)
      .then((output) => setReturnState(output.data))
  }

  useEffect(() => {
    const interval = setInterval(() => {
      if (btnActive) { stateToJSON(criticalState) };
    }, 10);
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
        intersectionType={intersectionValue}
        numCars={numCars}
        btnActive={btnActive}
        returnState={returnState}
        setValueForParent={setCarArray} />

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
          onClick={(event) => { setBtnActive(!btnActive); if (btnActive) stateToJSON(criticalState) }}>
          {btnActive ? "Pause" : "Begin"}
        </div>
      </div>
    </>
  )
}

export default App;

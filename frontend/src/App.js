import './App.css';
import { useState } from 'react';
import DropDown from './dropdown';
import World from './worldComponents';


const App = () => {

  /* UseState Hooks
      Forces a rerender of associated components when
      state variables change. */

  const [numCars, setNumCars] = useState(5);
  const [btnActive, setBtnActive] = useState(false);
  const [situationValue, setSituationValue] = useState('Any');
  const [intersectionValue, setIntersectionValue] = useState('4-Way Intersection');

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
        intersectionType={intersectionValue} />

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
          onClick={(event) => setBtnActive(!btnActive)}>
          {btnActive ? "Pause" : "Begin"}
        </div>
      </div>
    </>
  )
}

export default App;

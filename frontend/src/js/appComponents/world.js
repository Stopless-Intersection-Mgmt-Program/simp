import { Intersection } from './worldComponents/intersection.js'
import CarManager from './worldComponents/cars.js'

/* World 
    Acts as the parent div of all car divs, roads, and lanes. 
    Sets relative environment for positioning of cars and roadComponents 
    (Reminder: World dimensions must be 600x600 to ensure proper scaling for data passed from backend) */
const World = (props) => {
    return (
        <>
            <div id='world'
                style={{
                    height: props.worldHeight,
                    width: props.worldWidth,
                    position: 'relative',
                }}>
                <Intersection {...props} />
                <CarManager {...props} />
            </div>
        </>
    )
}

export default World;

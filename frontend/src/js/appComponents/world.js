import { Intersection } from './worldComponents/intersection.js'
import CarManager from './worldComponents/cars.js'

/* worldComponent passes all dimension props to intersectionComponent,
    and roadComponent, acts as the parent div of all car divs, roads, and lanes. 
    (Remember: set worldWidth, and worldHeight as a proportion of the
               max screen viewport not a default value.) */
const World = (props) => {
    return (
        <>
            <div id='world'
                style={{
                    height: props.worldHeight,
                    width: props.worldWidth,
                    position: 'absolute',
                    marginTop: '1%',
                    marginLeft: '30%',
                }}>
                <Intersection {...props} />
                <CarManager {...props} />
            </div>
        </>
    )
}

export default World;

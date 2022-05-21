
import { useEffect, useState, useLayoutEffect } from 'react';
import 'react-dom';

var roadsToRender = [];
let spawnBoxes = [];
let spawnedCars = [];
let carID = 0;


function detectCollision(r1, r2) {
    if (r1.x + r1.width >= r2.x &&     // r1 right edge past r2 left
        r1.x <= r2.x + r2.width &&       // r1 left edge past r2 right
        r1.y + r1.height >= r2.y &&       // r1 top edge past r2 bottom
        r1.y <= r2.y + r2.height) {       // r1 bottom edge past r2 top
        return true;
    }
    return false;
}

/* Car Component:
    renders a car object with coordinates/angle/startPoint/endPoint dependent on the Car Spawner,
    generates carid, car dimensions, speed, */
const CarComponent = (props) => {
    return (
        <div className="car"
            style={{
                carID: props.carID,
                height: 2 * 2.325,
                width: 4 * 2.2325, //Will generate random dimensions in sprint 4 
                left: props.left - 4 * 2.2325 / 2,
                top: props.top - 2 * 2.2325 / 2,
                transform: `rotate(${props.angle})`
            }}>
        </div>
    )
}


/* RenderTrafficLight checks if 'Traffic Light' is selected in algorithm dropdown menu
   renders traffic lights on roads if it is selected */
const RenderTrafficLight = (props) => {
    let render = []; 
    if (props.algorithmValue === "Traffic Light") {
        render.push(<span className='light' style={{height: 6, width: 6}}></span>); 
    } 
    
    return render; 
}


/* Road Component: renders a road amongst an intersection,
    Every class Road contains an arbitrary amount of lanes
    as a proportion of roadWidth */
const RoadComponent = (props) => {
    return (
        <div className="road"
            style={{
                margin: 0,
                height: props.roadWidth,
                width: props.roadLength,
                left: props.spacingLeft,
                top: props.spacingTop,
                transformOrigin: 'left center',
                transform: `rotate(${props.degrees})`
            }}>
            {/* Edit hardcode */}
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: .13 * props.roadWidth,
                    marginBottom: 0
                }} />
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: 2,
                    marginBottom: 0,
                }} />

            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: .10 * props.roadWidth,
                    marginBottom: 0,

                }}>
                <RenderTrafficLight algorithmValue={props.algorithmValue}></RenderTrafficLight>
            </div>
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: 2,
                    marginBottom: 0,
                }}>
                <RenderTrafficLight algorithmValue={props.algorithmValue}></RenderTrafficLight>
            </div>
        </div >
    )
}

/* Convert intersection type to road mappings for rendering */
const layoutMappings = {
    '4-Way Intersection': [1, 3, 5, 7],
    'T-Way Intersection': [1, 3, 5],
    'X-Way Intersection': [2, 4, 6, 8],
    'Multi-Way Intersection': [1, 2, 3, 4, 5, 6, 7, 8]
};

function degreesToCoords(radius, degrees, error) {
    return ([(300 + radius * Math.sin(Math.PI * (-90 + degrees) / 180)), (300 - radius * Math.cos(Math.PI * (-90 + degrees) / 180) - error)])
}

function RoadRenderer(props) {
    const roadWidth = .15 * props.worldWidth;
    const roadLength = props.worldHeight / 2;
    const intersectionType = props.intersectionType;

    roadsToRender = [];
    spawnBoxes = [];
    let coordinates = [];
    let degrees;

    layoutMappings[intersectionType].forEach((road) => {
        degrees = (road - 1) * 45;
        coordinates = degreesToCoords(roadLength, degrees, roadWidth / 2);
        //lights
        spawnBoxes.push(
            {
                x: coordinates[0],
                y: coordinates[1],
                width: roadWidth,
                height: roadLength / 6,
                start: road
            }
        );
        roadsToRender.push(
            <RoadComponent
                degrees={degrees + 'deg'}
                spacingLeft={coordinates[0]}
                spacingTop={coordinates[1]}
                roadWidth={roadWidth}
                roadLength={roadLength}
                algorithmValue={props.algorithmValue} />);
    })
    return (roadsToRender)
}

const CarSpawner = (props) => {
    //let carsToCheck = layoutMappings[props.intersectionType].length
    //let availableSpawns = [];
    useEffect(() => {
        for (var i = 0; i < spawnBoxes.length; i++) {
            let collisionFree = true;

            props.cars.forEach((car) => {
                if (detectCollision(car, spawnBoxes[i])) {
                    collisionFree = false;
                }
            })
            if (collisionFree) {
                //We dont talk about the carID
                props.setCars([...props.cars,
                {
                    'carID': props.cars[0] ? props.cars[props.cars.length - 1].carID.valueOf() + 1 : 0,
                    x: spawnBoxes[i].x,
                    y: spawnBoxes[i].y,
                    startingLane: spawnBoxes[i].start,
                    finishingLane: (layoutMappings[props.intersectionType])[Math.floor(Math.random() * layoutMappings[props.intersectionType].length)],
                    height: 4,
                    width: 12
                }])
                console.log("added car", props.cars)
                return;
            }
        }
    }, [props.intersectionType])
}


const CarManager = (props) => {
    useEffect(() => {
        const fetchState = async () => {
            spawnedCars = []
            let returnCars = await props.returnState
            returnCars.cars.forEach((car) => {
                spawnedCars.push(
                    <CarComponent
                        carID={car[0]}
                        left={car[1] * 2.325 + 300}
                        top={(-1 * car[2]) * 2.325 + 300}
                        angle={-1 * car[3] + 'rad'} />
                )
            })
        }
        fetchState()
    }, [props.returnState])
    return spawnedCars
}
/* IntersectionComponent: populates the center of the world div
    with an intersection, and a list of roads based on intersection type. */
const IntersectionComponent = (props) => {
    const intersectionLength = .15 * props.worldWidth + 2;
    return (
        <>
            <div className='intersection'
                style={{
                    height: intersectionLength - 1,
                    width: intersectionLength - 1,
                    marginTop: (props.worldHeight - intersectionLength) / 2,
                    marginLeft: (props.worldWidth - intersectionLength) / 2,
                    intersectionType: props.intersectionType
                }} />
            <RoadRenderer {...props}></RoadRenderer>
        </>
    )
}

/* worldComponent passes all dimension props to intersectionComponent,
    and roadComponent, acts as the parent div of all car divs, roads, and lanes. 
    (Remember: set worldWidth, and worldHeight as a proportion of the
               max screen viewport not a default value.) */
const World = (props) => {
    //Reset on intersectionType change
    let [cars, setCars] = useState([]);

    useEffect(() => {
        console.log("in effect", cars)
        props.setValueForParent(cars)
    }, [cars, setCars])

    console.log("world", props.returnState);
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
                <IntersectionComponent {...props} />

                {cars.length < props.numCars ?
                    <CarSpawner {...props} cars={cars} setCars={setCars} />
                    :
                    null
                }
                <CarManager {...props} cars={cars} setCars={setCars} />

            </div>
        </>
    )
}

export { World, layoutMappings };

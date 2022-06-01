import { useEffect, useState } from 'react'

let spawnedCars = [];

/* detectCollision 
    detects collision of two rectangles with properties: x,y,width,height
    returns True if there exists a collision, false otherwise*/
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
    let scale = 2.2325
    return (
        <div className="car"
            style={{
                carID: props.carID,
                height: 2 * 2.2325,
                width: 4 * 2.2325, //Will generate random dimensions in sprint 4 
                left: props.left - 5.5 * 2.2325 / 2,
                top: props.top - 3 * 2.2325 / 2,
                transform: `rotate(${props.angle})`,
                backgroundColor: `hsl(0, 100%, ${((props.speed / 30) * .5 + .5) * 100 + '%'})`
            }}>
        </div>
    )
}

/* CarManager
    updates list of car positions from the backend, 
    and renders them as CarComponents with scaling and shifting added to account for different coordinate systems.
    If car positions cannot be updated it renders the last tick. */
const CarManager = (props) => {
    useEffect(() => {
        //Constant for collision testing values never change.
        const world = {
            width: props.worldWidth,
            height: props.worldHeight,
            x: 0,
            y: 0
        }
        const fetchState = () => {
            let returnCars = props.returnState
            spawnedCars = [];
            returnCars.cars.forEach((car, index) => {
                let newCar = {
                    x: car[1] * 2.325 + 300,
                    y: -1 * car[2] * 2.2325 + 300,
                    width: 4 * 2.2325,
                    height: 2 * 2.2325
                }
                if (detectCollision(newCar, world)) {
                    spawnedCars.push(
                        <CarComponent
                            key={index}
                            carID={car[0]}
                            left={newCar.x}
                            top={newCar.y}
                            angle={-1 * car[3] + 'rad'}
                            speed={car[4]} />
                    )
                }
            })
        }

        fetchState()
    }, [props.returnState])
    return spawnedCars
}

export default CarManager;

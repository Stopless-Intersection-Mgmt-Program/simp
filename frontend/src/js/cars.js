import { useEffect } from 'react'
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
                height: 2 * 2.2325,
                width: 4 * 2.2325, //Will generate random dimensions in sprint 4 
                left: props.left - 4 * 2.2325 / 2,
                top: props.top - 2 * 2.2325 / 2,
                transform: `rotate(${props.angle})`
            }}>
        </div>
    )
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

export default CarManager;

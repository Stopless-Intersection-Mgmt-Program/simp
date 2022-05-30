var roadsToRender = [];
let spawnBoxes = [];

/* Convert intersection type to road mappings for rendering */
const layoutMappings = {
    '4-Way Intersection': [0, 1, 2, 3],
    'T-Way Intersection': [0, 1, 2],
    'T-Way Flipped': [0, 2, 3]
};

function degreesToCoords(radius, degrees, error) {
    return ([(300 + radius * Math.sin(Math.PI * (-90 + degrees) / 180)), (300 - radius * Math.cos(Math.PI * (-90 + degrees) / 180) - error)])
}


/* RenderTrafficLight checks if 'Traffic Light' is selected in algorithm dropdown menu
   renders traffic lights on roads if it is selected */
const RenderTrafficLight = (props) => {
    let render;
    if (props.returnState.lanesCleared != undefined) {
        let laneCleared = props.returnState.lanesCleared[props.road]
        let colorValue = laneCleared ? 'rgb(0,255,0)' : 'rgb(255,0,0)';
        render = (<span className='light' style={{ height: 6, width: 6, backgroundColor: { colorValue } }} />);
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

                }} >
                <RenderTrafficLight returnState={props.returnState} road={props.road}></RenderTrafficLight>
            </div>
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: 2,
                    marginBottom: 0,
                }} >
                <RenderTrafficLight returnState={props.returnState} road={props.road} ></RenderTrafficLight>
            </div>
        </div >

    )
}

function RoadRenderer(props) {
    const roadWidth = .15 * props.worldWidth;
    const roadLength = props.worldHeight / 2;
    const intersectionType = props.intersectionType;
    roadsToRender = [];
    spawnBoxes = [];
    let coordinates = [];
    let degrees;

    layoutMappings[intersectionType].forEach((road, index) => {
        degrees = (road) * 90;
        coordinates = degreesToCoords(roadLength, degrees, roadWidth / 2);
        roadsToRender.push(
            <RoadComponent
                key={index}
                degrees={degrees + 'deg'}
                spacingLeft={coordinates[0]}
                spacingTop={coordinates[1]}
                roadWidth={roadWidth}
                roadLength={roadLength}
                returnState={props.returnState}
                road={road} />);
    })
    return (roadsToRender)
}

/* IntersectionComponent: populates the center of the world div
with an intersection, and a list of roads based on intersection type. */
const Intersection = (props) => {
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

export { Intersection, layoutMappings };
import '../../../css/appComponents/worldComponents/intersection.css'

var roadsToRender = [];
let spawnBoxes = [];

/* Convert intersection type to road mappings for rendering */
const layoutMappings = {
    '4-Way Intersection': [0, 1, 2, 3],
    'T-Way Intersection': [0, 1, 2],
    'T-Way Flipped': [0, 2, 3]
};

/* degreesToCoords
    returns x,y positions around a circle of radius based on degrees
    Shifted by 300 pixels to account for x,y starting from the top-left
    degrees are shifted back 90 degrees to account for relative starting position
    error: the vertical shift required after performing `transform(rotate(deg))` to ensure div start is at x,y */
function degreesToCoords(radius, degrees, error) {
    return ([(300 + radius * Math.sin(Math.PI * (-90 + degrees) / 180)), (300 - radius * Math.cos(Math.PI * (-90 + degrees) / 180) - error)])
}


/* RenderTrafficLight 
    checks if 'Traffic Light' is selected in algorithm dropdown menu
    renders traffic lights on roads if it is selected */
const RenderTrafficLight = (props) => {
    let render;

    if (props.returnState.lanesCleared != undefined) {
        let laneCleared = props.returnState.lanesCleared[props.road][props.lane]
        let colorValue = laneCleared ? 'rgb(0,255,0)' : 'rgb(255,0,0)';
        render = (<span className='light' style={{ height: 6, width: 6, backgroundColor: colorValue }} />);
    }

    return render;
}

/* Road Component: renders a road div
    Every Road contains 4 lane div as a proportion of roadWidth.
    Every Road's length is defined by roadLength which is the width of the world  */
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
                <RenderTrafficLight returnState={props.returnState} road={props.road} lane={1}></RenderTrafficLight>
            </div>
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: 2,
                    marginBottom: 0,
                }} >
                <RenderTrafficLight returnState={props.returnState} road={props.road} lane={0} ></RenderTrafficLight>
            </div>
        </div >

    )
}

/* RoadRenderer
    Given a layout[intersectionValue] from layoutMappings
    calculates position of each Road around the intersection, 
    and populates the intersection component with the corresponding RoadComponents */
function RoadRenderer(props) {
    const roadWidth = .15 * props.worldWidth;
    const roadLength = props.worldHeight / 2;
    const intersectionType = props.intersectionType;
    roadsToRender = [];
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
                road={index} />);
    })
    return (roadsToRender)
}

/* IntersectionComponent
    populates the center of the world div with an intersection, and a list of roads based on intersection type. */
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
                    intersectionType: props.intersectionType,
                }} />
            <RoadRenderer {...props}></RoadRenderer>
        </>
    )
}

export { Intersection, layoutMappings };
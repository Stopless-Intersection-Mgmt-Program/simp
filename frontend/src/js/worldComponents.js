
import { useEffect } from 'react';
import 'react-dom';


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

                }} />
            <div className="lane"
                style={{
                    height: 0.15 * props.roadWidth,
                    marginTop: 2,
                    marginBottom: 0,
                }} />
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

    let roadsToRender = [];
    let coordinates = [];
    let degrees;

    layoutMappings[intersectionType].forEach((road) => {
        degrees = (road - 1) * 45;
        coordinates = degreesToCoords(roadLength, degrees, roadWidth / 2);
        roadsToRender.push(
            <RoadComponent
                degrees={degrees + 'deg'}
                spacingLeft={coordinates[0]}
                spacingTop={coordinates[1]}
                roadWidth={roadWidth}
                roadLength={roadLength} />)
    })
    return (roadsToRender)
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
    return (
        <>
            <div id='world'
                style={{
                    height: props.worldHeight,
                    width: props.worldWidth,
                    position: 'absolute',
                    marginTop: '1%',
                    marginLeft: '30%',
                }} >
                <IntersectionComponent {...props} />
            </div>
        </>
    )
}

export default World;
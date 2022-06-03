import '../../../css/appComponents/worldComponents/statistics.css'

const DisplayStatistics = (props) => {
    if (props.statistics != undefined) {
        return (
            <div className='statisticsWrapper'>
                <div className='stats'>
                    Throughput: {props.statistics[2].toFixed(2)}
                </div>
                <div className='stats'>
                    Wait Time: {props.statistics[0].toFixed(2)}
                </div>
                <div className='stats'>
                    Avg Speed: {props.statistics[1].toFixed(2)}
                </div>
            </div>
        );
    }
    else {
        return null;
    }
}

export default DisplayStatistics; 
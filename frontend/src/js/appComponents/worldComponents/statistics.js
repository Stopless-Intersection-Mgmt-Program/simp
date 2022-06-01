import { useEffect, useState } from 'react'

const DisplayStatistics = (props) => {
    if (props.statistics != undefined) {
        return (
            <div className='statisticsWrapper'>
                <div className='stats'>
                    Wait Time: {"\n" + props.statistics[0]}
                </div>
                <div className='stats'>
                    Throughput: {"\n" + props.statistics[2]}
                </div>
                <div className='stats'>
                    Average Speed: {"\n" + props.statistics[1]}
                </div>
            </div>
        );
    }
    else {
        return null;
    }
}

export default DisplayStatistics; 
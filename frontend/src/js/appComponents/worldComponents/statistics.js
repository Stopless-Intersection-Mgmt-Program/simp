import { useEffect, useState } from 'react'
import '../../../css/statistics.css';

const DisplayStatistics = (statistics) => {
    console.log(statistics);
    if (statistics != undefined) {
        return(
            <div className='statisticsWrapper'>
                <div className='stats'>
                    Wait Time: {statistics.waitTime} 
                </div>
                <div className='stats'>
                    Throughput: {statistics.throughput}
                </div>
                <div className='stats'>
                    Average Speed: {statistics.averageSpeed}
                </div>
            </div> 
        );  
    }
    else {
        return null; 
    }
}

export default DisplayStatistics; 
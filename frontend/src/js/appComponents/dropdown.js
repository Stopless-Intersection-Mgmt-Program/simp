import { useState } from 'react';

const DropDown = (props) => {

    const optionsArray = props.options;
    const [dropDownValue, setDropDownValue] = useState()

    return (
        <>
            <label htmlFor={props.name}>{props.name}</label>
            <select className="dropDown"
                id={props.name}
                onClick={(event) => event.stopPropagation()}
                value={dropDownValue}
                onChange={(event) => { setDropDownValue(event.target.value); if (props.setValueForParent) { props.setValueForParent(event.target.value) } }}>
                {optionsArray.map((optionsElement) => <option key={optionsElement} value={optionsElement}>{optionsElement}</option>)}
            </select>
        </>
    )
}

export default DropDown;

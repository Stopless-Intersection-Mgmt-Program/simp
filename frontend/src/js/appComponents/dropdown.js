import '../../css/appComponents/dropdown.css'
import { useState } from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

/* DropDown
    Renders a UI dropdown using Material UI
    Props
        name: ties InputLabel and Select id's to name and renders name as dropdown label text
        default: sets default value for dropdown placeholder value to be rendered
        setValueForParent: Updates parent useState when values change using corresponding setState
        options: an array of values to populate the dropdown menu */
const DropDown = (props) => {

    const optionsArray = props.options;
    const [dropDownValue, setDropDownValue] = useState(props.default)

    return (
        <FormControl fullWidth>
            <InputLabel id={props.name} style={{ color: '#80959B' }}>{props.name}</InputLabel>
            <Select
                sx={{
                    "& .MuiOutlinedInput-input": {
                        color: '#80959B'
                    },
                    "& .MuiSvgIcon-root": {
                        color: "#80959B",
                    },
                }}
                className='dropDown'
                labelId={props.name}
                id={props.name}
                size={'small'}
                value={dropDownValue}
                label={props.name}
                onChange={(event) => {
                    setDropDownValue(event.target.value);
                    if (props.setValueForParent) {
                        props.setValueForParent(event.target.value)
                    }
                }}
                displayEmpty>
                {optionsArray.map((optionsElement) => <MenuItem style={{ color: '#80959B', selectedTextColor: '#80959B' }} key={optionsElement} value={optionsElement}>{optionsElement}</MenuItem>)}
            </Select>
        </FormControl>
    )
}

export default DropDown;

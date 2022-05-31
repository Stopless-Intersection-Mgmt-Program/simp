import { useState } from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';


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

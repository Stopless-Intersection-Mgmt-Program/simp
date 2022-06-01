/* Button
    Renders a button UI component.
    Props
        func: Function to be run when button is clicked
        arg: Function arg/s to be run when button is clicked
        name: Rendered text within the button component
    Buttons have two functionalities on user click:
        1. Triggers an ApiCall with 3 arguments
        2. Triggers a true/false switch useState */
const Button = (props) => {
    return (
        <div
            id='btn'
            className='btn'
            width="auto"
            onClick={(event) => { Array.isArray(props.arg) ? props.func(props.arg[0], props.arg[1], props.arg[2]) : props.func(!props.arg) }}>
            {props.name}
        </div>
    )
}

export default Button;



const Button = (props) => {
    console.log("wopoo", props.arg, props.name);
    console.log(Array.isArray(props.arg));
    return (
        <div
            id='btn'
            className='btn'
            width="100%"
            onClick={(event) => { Array.isArray(props.arg) ? props.func(props.arg[0], props.arg[1], props.arg[2]) : props.func(!props.arg) }}>
            {props.name}
        </div>
    )
}

export default Button;
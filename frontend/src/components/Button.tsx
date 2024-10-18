interface ButtonProps {
    text: string
    type?: 'button' | 'submit' | 'reset'
  }
  
  export default function Button({ text, type = 'button' }: ButtonProps) {
    return (
      <button type={type} className="buttonStyle">
        {text}
      </button>
    )
  }
  
  export {}
  
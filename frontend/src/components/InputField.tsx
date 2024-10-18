interface InputFieldProps {
    type: string
    placeholder: string
    value: string
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
    required?: boolean
  }
  
  export default function InputField({
    type,
    placeholder,
    value,
    onChange,
    required = false
  }: InputFieldProps) {
    return (
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        className="inputStyle"
      />
    )
  }
  
  export {}
  
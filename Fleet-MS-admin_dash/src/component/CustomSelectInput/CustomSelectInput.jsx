import { useState } from "react";

import { useField } from "formik";
import { Form, InputGroup, Placeholder } from "react-bootstrap";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const CustomSelectInput = ({ type, icon, label, options , placeholder, ...props }) => {
  const [field, meta] = useField(props);
  
 
  return (
    <Form.Group className="p-2">
      {label ? (
        <Form.Label>
          {label}
          <span className="text-danger"> *</span>
        </Form.Label>
      ) : null}
      <InputGroup hasValidation>
        <InputGroup.Text>
          <FontAwesomeIcon icon={icon} />
        </InputGroup.Text>
        <Form.Select
          {...field}
          {...props}
          isInvalid={meta.touched && !!meta.error}
          isValid={meta.touched && !Boolean(meta.error)}
          className={ meta.value === placeholder && 'text-muted' } 
        >
         <option className='text-muted' key={10}>{placeholder}</option>
         {options.map((e,index)=>{
          return (
            <>
            
            <option key={index} value={e.type}>{e.type}</option>
            </>
          )
         })}
          
        </Form.Select>

        <Form.Control.Feedback className="alert alert-danger" type="invalid">
          {meta.error}
        </Form.Control.Feedback>
      </InputGroup>
    </Form.Group>
  );
};
export default CustomSelectInput;

import React from 'react'
import {Stack , Form , InputGroup} from 'react-bootstrap'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const SingleInformationInput = ({label , placeholder , icon}) => {
  return (
    <Stack>
    <Form.Label className='text-success'>{label}</Form.Label>  
    <InputGroup hasValidation>
        <InputGroup.Text>
          <FontAwesomeIcon icon={icon} />
        </InputGroup.Text>
      
        <Form.Control  placeholder={placeholder} readOnly />
       
      </InputGroup>
    
  </Stack>
  )
}

export default SingleInformationInput
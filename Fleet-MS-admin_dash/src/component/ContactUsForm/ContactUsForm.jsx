import React from 'react'
import { Stack, Container } from 'react-bootstrap'
import SingleInformationInput from '../SingleInformationInput/SingleInformationInput'
import { faEnvelope, faPhone, faMapLocation } from "@fortawesome/free-solid-svg-icons";
import SocialLinks from '../SocialLinks/SocialLinks';
const ContactUsForm = () => {
  return (
    <>
      <Stack className='px-5 pt-3' gap={3}>
        <SingleInformationInput label='Our Email' placeholder='FastX@gmail.com' icon={faEnvelope} />
        <SingleInformationInput label='Our Phone' placeholder='01156121177' icon={faPhone} />
        <SingleInformationInput label='Our Address' placeholder='El Shorouk City' icon={faMapLocation} />
        <SocialLinks />
      </Stack>

    </>
  )
}

export default ContactUsForm
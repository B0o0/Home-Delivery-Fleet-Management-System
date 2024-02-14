import React from 'react'
import {Placeholder} from 'react-bootstrap'
const SkeltonLoader = () => {
  return (
    <>
          <Placeholder as="p" animation="glow">
            <Placeholder xs={12} />
          </Placeholder>
          <Placeholder as="p" animation="glow">
            <Placeholder xs={12} />
          </Placeholder>
          <Placeholder as="p" animation="glow">
            <Placeholder xs={12} />
          </Placeholder>
        </>
  )
}

export default SkeltonLoader
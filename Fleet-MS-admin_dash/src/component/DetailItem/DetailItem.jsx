import React from "react";

const DetailItem = ({ title, txt }) => {
  return (
    <div className='m-3 p-3'>
      <p
        className="display-6 border-bottom border-3 border-info "
        style={{ width: "max-content" }}
      >
        {title}
      </p>
      <p className="m-auto display-6 text-muted border-bottom border-1">
        {txt}
      </p>
    </div>
  );
};

export default DetailItem;

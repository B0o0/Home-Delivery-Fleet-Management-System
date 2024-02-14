import React from "react";
import MainPageText from "../../component/MainPageText/MainPageText";
import AddAdminForm from "../../component/AddAdminForm/AddAdminForm";

const AddAdmin = () => {
  return (
    <div className="container-fluid">
      <MainPageText text="Add New Admin" />
      <AddAdminForm />
    </div>
  );
};

export default AddAdmin;

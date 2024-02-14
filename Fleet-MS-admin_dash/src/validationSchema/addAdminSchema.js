import * as Yup from "yup";


const addAdminSchema = Yup.object().shape({
  username: Yup.string()
    .trim()
    .matches(/^[aA-zZ\s]+$/, "Only alphabets are allowed for this field ")
    .min(3, "Too Short!")
    .max(50, "Too Long!")
    .required("Name Required"),
  
  email: Yup.string()
    .trim()
    .email("Enter A valid Email")
    .required("E-Mail Required"),
  password : Yup.string().max(20 , "Max Length is 20").min(3 , "Min Length is 8").required('Password Require') ,  
  confirm_password : Yup.string()
  .oneOf([Yup.ref('password'), null], 'Passwords must match') ,
  phone: Yup.string()
    .min(11, "Phone Must Be 11 number")
    .max(11, "Phone Must Be 11 number")
    .required("Phone Required")
    .test("startWith", "Must start With 010 || 011 || 012 ", (value) => {
      return (
        value.startsWith("010") ||
        value.startsWith("011") ||
        value.startsWith("012")
      );
    }),
 
});

export default addAdminSchema;

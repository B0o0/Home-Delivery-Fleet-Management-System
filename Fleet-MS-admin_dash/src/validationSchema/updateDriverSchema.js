import * as Yup from "yup";

const updateDriverSchema = Yup.object().shape({
  first_name: Yup.string()
    .trim()
    .matches(/^[aA-zZ\s]+$/, "Only alphabets are allowed for this field ")
    .min(3, "Too Short!")
    .max(50, "Too Long!")
    .required("Name Required"),
    last_name: Yup.string()
    .trim()
    .matches(/^[aA-zZ\s]+$/, "Only alphabets are allowed for this field ")
    .min(3, "Too Short!")
    .max(50, "Too Long!")
    .required("Name Required"),  
  
  email: Yup.string()
    .trim()
    .email("Enter A valid Email")
    .required("E-Mail Required"),
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
  address: Yup.string()
    .min(10, "Address In Detail Please")
    .max(100, "This Address Is Too Long")
    .required("Address Required"),
    licence_id : Yup.string()
    .min(14, "Licence Must Be 14 chars")
    .max(14, "Licence Must Be 14 chars")
    .required("Licence Id Required"),
});

export default updateDriverSchema;

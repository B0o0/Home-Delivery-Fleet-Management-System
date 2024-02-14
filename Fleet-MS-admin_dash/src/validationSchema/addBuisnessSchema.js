import * as Yup from "yup";
const URL =
  /^((https?|ftp):\/\/)?(www.)?(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i;

const addBuisnessSchema = Yup.object().shape({
  name: Yup.string()
    .trim()
    .matches(/^[aA-zZ\s]+$/, "Only alphabets are allowed for this field ")
    .min(3, "Too Short!")
    .max(50, "Too Long!")
    .required("Name Required"),
  contact_name: Yup.string()
    .trim()
    .matches(/^[aA-zZ\s]+$/, "Only alphabets are allowed for this field ")
    .min(3, "Too Short!")
    .max(50, "Too Long!")
    .required("Name Required"),

  business_website: Yup.string().matches(URL, "Enter a valid url").required('WebSite Is Require'),
  postal_code: Yup.string()
    .max(15, "Max Postal code is 15")
    .min(5, "It Must at least 5")
    .required("postal code required"),
  email: Yup.string()
    .trim()
    .email("Enter A valid Email")
    .required("E-Mail Required"),
  password : Yup.string().max(20 , "Max Length is 20").min(3 , "Min Length is 8").required('Buisness Password Require') ,  
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
  type: Yup.string()
    .oneOf(["Market", "Restaurant"], "Just Resturant or Market")
    .required("Type Of Required"),
  address: Yup.string()
    .min(10, "Address In Detail Please")
    .max(50, "This Address Is Too Long")
    .required("Address Required"),
});

export default addBuisnessSchema;

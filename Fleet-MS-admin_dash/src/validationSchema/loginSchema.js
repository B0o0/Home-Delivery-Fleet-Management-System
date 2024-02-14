import * as Yup from "yup";

const loginSchema = Yup.object().shape({
  email: Yup.string()
    .trim()
    .email("Enter A valid Email")
    .required("E-Mail Required"),
  password: Yup.string()
    .max(20, "Max Length is 20")
    .min(3, "Min Length is 8")
    .required("Buisness Password Require"),
});

export default loginSchema;

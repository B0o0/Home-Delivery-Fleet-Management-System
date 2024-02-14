import { Stack, Image } from "react-bootstrap";
import TouchImage from "../../assets/images/touch.png";
import AnalysticsImage from "../../assets/images/anal.png";
import ActionImage from "../../assets/images/action.png";
const Banner = () => {
  return (
    <Stack
      gap={2}
      className="justify-content-center align-items-center col-lg-7 col-md-12"
      
    >
      <div className="w-100 d-flex justify-content-center align-items-center">
        <p className="display-6" style={{ fontFamily: "Dancing Script" }}>
          Business Mangment
        </p>
        <Image src={TouchImage} className="m-3" style={{ width: "14%" }} />
      </div>
      <div className="d-flex justify-content-center align-items-center">
        <Image src={ActionImage} className="m-3" style={{ width: "14%" }} />
        <p
          className="text-primary display-6"
          style={{ fontFamily: "Dancing Script" }}
        >
          Take Actions And Adminstration{" "}
        </p>
      </div>
      <div className="d-flex justify-content-center align-items-center">
        <p className="display-6" style={{ fontFamily: "Dancing Script" }}>
          All Statics In Your Hand
        </p>
        <Image src={AnalysticsImage} className="m-3" style={{ width: "14%" }} />
      </div>
    </Stack>
  );
};

export default Banner;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { IoArrowBack } from 'react-icons/io5';


const Profile =()=>{
    const navigate=useNavigate();
    
    const [firstName,setFirstName]=useState("");
    const [lastname, setlastname] = useState("");
    const [image,setImage] = useState("");
    const [hoverd,setHoverd] = useState(false);
    const [selectedColor, setselectedColor] = useState(0);

    const saveChanges = async()=>{};
    return(
        <div className="bg-[#1b1c24] h-[100vh] flex items-center justify-center flex-col gap-10">
        <div className="flex flex-col gap-10 w-[80vw] md:w-max"></div>
        <div>   
        <IoArrowBack className='text-4xl lg:text-6xl text-white/90 cursor-pointer' />
        <div className="grid grid-cols-2">
            <div  className="h-full w-32 md:w-48 md:h-48 relative flex items-center justify-center"
            onMouseEnter={()=>setHoverd(true)}
            onMouseLeave={()=>setHoverd(false)}
            >


            </div>
        </div>
        </div>
        </div>
    );
}

export default Profile;
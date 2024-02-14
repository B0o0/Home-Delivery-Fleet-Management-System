const leftNavActions = [
  {
    link: '/map' , 
    listAction : 'Map View' , 
    icon : 'fa-solid fa-map-location-dot'
  } ,
  {
    lists: [
      { link: "/buisness", txt: "All Business" },
      { link: "/addBuisness", txt: "Add New Business" },
      { link: "/pendingBuisness", txt: "Pending Business" },
    ],
    listAction: "Manage Business",
    icon : 'fa-solid fa-business-time' ,
  },
  {
    lists: [
      { link: "/orders", txt: "All Orders" },
    ],
    listAction: "Manage Orders",
    icon : 'fa-solid fa-cart-shopping'
  },
  
  {
    lists: [
      { link: "/customers", txt: "All Customers" },
    ],
    listAction: "Manage Customers",
    icon : 'fas fa-users'
  },
  {
    lists: [
      { link: "/drivers", txt: "All Drivers" },
      { link: "/pendingDrivers", txt: "Pending Drivers" },
      
    ],
    listAction: "Manage Drivers",
    icon : 'fa-solid fa-motorcycle'
  },
  {
    link : '/contactus' , 
    listAction: "Contact Us",
    icon : 'fa-solid fa-address-book'
  },
  
];

export default leftNavActions

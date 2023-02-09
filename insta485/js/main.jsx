import React from "react";
import { createRoot } from "react-dom/client";
import Index from "./index";


const root = createRoot(document.getElementById("reactEntry"));
root.render(<Index/>);
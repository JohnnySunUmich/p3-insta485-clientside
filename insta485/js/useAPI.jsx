import { useState, useEffect} from 'react';

export default function useAPI(url, urlMethod, depenArr, cond, switchFunc) {
    const [data, setData] = useState(null);
    useEffect(() => {
        (async () => {
            if (cond) {
                try {
                    switchFunc();
                    let bool = false;
                    const response = await fetch(url, { method: urlMethod, credentials: "same-origin" });
                    if (!response.ok) throw Error(response.statusText);
                    const json = await response.json();
                    if (!bool) setData(json)
                    return () => bool = true;   //Cleanup function whenever Post component unmounts or re-renders. Avoid updating state if a Post is about to unmount or re-render.
                }
                catch (error) {console.log(error);}
            }
        })();
    }, depenArr);
    return data;
}
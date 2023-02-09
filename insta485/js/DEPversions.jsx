// Version 1: Use promises
useEffect(() => {
    let ignoreStaleRequest = false;  //Declare a boolean flag that we can use to cancel the API request.

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
        .then(response => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then(data => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
                setRender(true);
                setData(data);
                setUserLiked(data.likes.lognameLikesThis);
                setNumLikes(data.likes.numLikes);
                setLikeUrl(data.likes.url);
            }
        })
        .catch(error => console.log(error));

    return () => {
        // This is a cleanup function that runs whenever the Post component unmounts or re-renders. If a Post is about to unmount or re-render, we should avoid updating state.
        ignoreStaleRequest = true;
    };
}, [url]);


// Version 2: Use async await
useEffect(() => {
    (async () => {
        try {
            setFetchedPost(false);
            let ignoreStaleRequest = false;  //To cancel the API request.
            const response = await fetch(url, { credentials: "same-origin" });
            if (!response.ok) throw Error(response.statusText);
            const data = await response.json();
            if (!ignoreStaleRequest) {
                setFetchedPost(true);
                setData(data);
                setInfoBar({postLink: data.postShowUrl, timeCreated: data.created, poster: data.owner, pfp: data.ownerImgUrl, posterLink: data.ownerShowUrl});
                setLikes({userLiked: data.likes.lognameLikesThis, num: data.likes.numLikes, url: data.likes.url});
            }
            return () => ignoreStaleRequest = true;   //Cleanup function whenever Post component unmounts or re-renders. Avoid updating state if a Post is about to unmount or re-render.
        }
        catch (error) {console.log(error);}
    })();
}, [url]);


// Version 3: Improved
// useEffect(() => {   //state already changed at likeUnlike
//     (async () => {
//         if (fetchedPost && clickedLikeBtn) {
//             try {
//                 setClickedLikeBtn(false);
//                 let bool = false;
//                 const response = await fetch(likes.userLiked ? `/api/v1/likes/?postid=${ data.postid }` : likes.url, { method: likes.userLiked ? "POST" : "DELETE", credentials: "same-origin" });
//                 if (!response.ok) throw Error(response.statusText);
//                 if (likes.userLiked) {
//                     const json = await response.json();
//                     if (!bool) setLikes(prev => ({...prev, url: json.url}));
//                 }
//                 return () => bool = true;
//             }
//             catch (error) {console.log(error);}
//         }
//     })();
// }, [likes.userLiked, likes.num]);
// const likeUnlike = () => {
//     setLikes(prev => ({...prev, userLiked: !prev.userLiked, num: prev.userLiked ? prev.num - 1 : prev.num + 1}));
//     setClickedLikeBtn(true);
// };

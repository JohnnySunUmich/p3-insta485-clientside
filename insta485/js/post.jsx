import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfoBar from "./infobar";
import Likes from "./likes";
import Comments from "./comments";


// The parameter of this function is an object with a string called url inside it.
export default function Post({ url }) {
    /* Display image and post owner of a single post */
    const [fetchedPost, setFetchedPost] = useState(false);
    const [data, setData] = useState({});
    const [infoBar, setInfoBar] = useState({});

    const [likes, setLikes] = useState({});
    const [clickedLikeBtn, setClickedLikeBtn] = useState(false);

    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState("");
    const [cmtSwitch, setCmtSwitch] = useState(false);
    const [clickedDelBtn, setClickedDelBtn] = useState(false);
    const [cmtToDel, setCmtToDel] = useState(null);

    const [doubleClickable, setDoubleClickable] = useState(false);
    const [doubleClicked, setDoubleClicked] = useState(false);
    
    // useEffect(() => {
    //     let ignoreStaleRequest = false;  //Declare a boolean flag that we can use to cancel the API request.

    //     // Call REST API to get the post's information
    //     fetch(url, { credentials: "same-origin" })
    //         .then(response => {
    //             if (!response.ok) throw Error(response.statusText);
    //             return response.json();
    //         })
    //         .then(data => {
    //             // If ignoreStaleRequest was set to true, we want to ignore the results of the request. Otherwise, update the state to trigger a new render.
    //             if (!ignoreStaleRequest) {
    //                 setRender(true);
    //                 setData(data);
    //                 setUserLiked(data.likes.lognameLikesThis);
    //                 setNumLikes(data.likes.numLikes);
    //                 setLikeUrl(data.likes.url);
    //             }
    //         })
    //         .catch(error => console.log(error));

    //     return () => {
    //         // This is a cleanup function that runs whenever the Post component unmounts or re-renders. If a Post is about to unmount or re-render, we should avoid updating state.
    //         ignoreStaleRequest = true;
    //     };
    // }, [url]);

    useEffect(() => {
        (async () => {
            try {
                setFetchedPost(false);
                let ignoreStaleRequest = false;  //To cancel the API request.
                const response = await fetch(url, { credentials: "same-origin" });
                if (!response.ok) throw Error(response.statusText);
                const json = await response.json();
                if (!ignoreStaleRequest) {
                    setFetchedPost(true);
                    setData(json);
                    setInfoBar({postLink: json.postShowUrl, timeCreated: json.created, poster: json.owner, pfp: json.ownerImgUrl, posterLink: json.ownerShowUrl});
                    setLikes({userLiked: json.likes.lognameLikesThis, num: json.likes.numLikes, url: json.likes.url});
                    setComments(json.comments);
                }
                return () => ignoreStaleRequest = true;   //Cleanup function whenever Post component unmounts or re-renders. Avoid updating state if a Post is about to unmount or re-render.
            }
            catch (error) {console.log(error);}
        })();
    }, [url]);

    // const likeUnlike = async () => {
    //     // setUserLiked(!userLiked); setNumLikes(userLiked ? numLikes - 1 : numLikes + 1);
    //     setLikes(prev => ({...prev, userLiked: !prev.userLiked, num: prev.userLiked ? prev.num - 1 : prev.num + 1}));   //async, may not be reflected immediately (possibly in the next rendering), depends on the updated state
    //     // setLikes({userLiked: !userLiked, num: userLiked ? n - 1 : n + 1, url: likes.url});
    //     try {
    //         const response = await fetch(likes.userLiked ? likes.url : `/api/v1/likes/?postid=${ data.postid }`, { method: likes.userLiked ? "DELETE" : "POST", credentials: "same-origin" });
    //         if (!response.ok) throw Error(response.statusText);
    //         if (!likes.userLiked) {
    //             const data = await response.json();
    //             setLikes(prev => ({...prev, url: data.url}));
    //         }
    //     }
    //     catch (error) {console.log(error);}
    // }


    useEffect(() => {   //state already changed at likeUnlike
        (async () => {
            if (fetchedPost) {
                try {
                    let bool = false;
                    const response = await fetch(likes.userLiked ? `/api/v1/likes/?postid=${ data.postid }` : likes.url, { method: likes.userLiked ? "POST" : "DELETE", credentials: "same-origin" });
                    if (!response.ok) throw Error(response.statusText);
                    if (likes.userLiked) {
                        const json = await response.json();
                        if (!bool) setLikes(prev => ({...prev, url: json.url}));
                    }
                    setDoubleClickable(false);
                    return () => bool = true;
                }
                catch (error) {console.log(error);}
            }
        })();
    }, [clickedLikeBtn]);
    const likeUnlike = () => {
        setLikes(prev => ({...prev, userLiked: !prev.userLiked, num: prev.userLiked ? prev.num - 1 : prev.num + 1}));
        setClickedLikeBtn(!clickedLikeBtn);
    };
    
    useEffect(() => {
        (async () => {
            if (fetchedPost) {
                try {
                    let bool = false;
                    const response = await fetch(`/api/v1/comments/?postid=${ data.postid }`, { method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: newComment}), credentials: "same-origin" });
                    if (!response.ok) throw Error(response.statusText);
                    const json = await response.json();
                    if (!bool) setComments([...comments, json]);
                    setNewComment("");
                    return () => bool = true;
                }
                catch (error) {console.log(error);}
            }
        })();
    }, [cmtSwitch]);
    const commented = e => {
        e.preventDefault();
        setCmtSwitch(!cmtSwitch);
    };

    useEffect(() => {
        (async () => {
            if (fetchedPost) {
                try {
                    let bool = false;
                    const response = await fetch(`/api/v1/comments/${ cmtToDel }/`, {method: "DELETE", credentials: "same-origin"});
                    if (!response.ok) throw Error(response.statusText);
                    const getUpdatedCmts = await fetch(`api/v1/posts/${ data.postid }/`, {credentials: "same-origin"});
                    if (!getUpdatedCmts.ok) throw Error(response.statusText);
                    const json = await getUpdatedCmts.json();
                    if (!bool) setComments(json.comments);
                    return () => bool = true;
                }
                catch (error) {console.log(error);}
            }
        })();
    }, [clickedDelBtn]);
    const deleteComment = (key) => {
        setCmtToDel(key);
        setClickedDelBtn(!clickedDelBtn);
    };

    useEffect(() => {
        (async () => {
            if (fetchedPost && doubleClickable && doubleClicked) {
                try {
                    setDoubleClicked(false);
                    let bool = false;
                    const response = await fetch(`/api/v1/likes/?postid=${ data.postid }`, { method: "POST", credentials: "same-origin" });
                    if (!response.ok) throw Error(response.statusText);
                    const json = await response.json();
                    if (!bool) setLikes(prev => ({...prev, url: json.url}));
                    return () => bool = true;
                }
                catch (error) {console.log(error);}
            }
        })();
    }, [doubleClickable]);
    const doubleClickToLike = () => {
        if (!likes.userLiked) {
            setLikes(prev => ({...prev, userLiked: true, num: prev.num + 1}));
            setDoubleClicked(true);
            setDoubleClickable(true);
        }
    };

    // Render post image and post owner
    return (
        fetchedPost &&
        <div className="post index">
            {/* { data.postid } */}
            <InfoBar { ...infoBar}/>
            <div className="content">
                <div className="pic" onDoubleClick={ doubleClickToLike }><img src={ data.imgUrl } alt={`${ data.owner }'s ${ data.created } post`}/></div>
                <div className="remaining">
                    <Likes userLiked={ likes.userLiked } numLikes={ likes.num } func={ likeUnlike }/>
                    <Comments comments={ comments } val={ newComment } onChange={ setNewComment } onSubmit={ commented } onClick={ deleteComment }/>
                </div>
            </div>
        </div>
    );
}

Post.propTypes = {
    url: PropTypes.string.isRequired,
};

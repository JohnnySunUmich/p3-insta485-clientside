import React from "react";

export default function Likes({ userLiked, numLikes, func }) {
    return (
        <>
            <button className="like-unlike-button" onClick={ func }>{`${(userLiked) ? "unlike" : "like"}`}</button>
            <div className="like">{`${numLikes} ${(numLikes === 1) ? " like" : " likes"}`}</div>
        </>
    );
}
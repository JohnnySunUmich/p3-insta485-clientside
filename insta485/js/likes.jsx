import React from "react";
import PropTypes from "prop-types";

export default function Likes({ userLiked, numLikes, func }) {
  return (
    <>
      <button type="submit" className="like-unlike-button" onClick={func}>{`${
        userLiked ? "unlike" : "like"
      }`}</button>
      <div className="like">{`${numLikes} ${
        numLikes === 1 ? " like" : " likes"
      }`}</div>
    </>
  );
}

Likes.propTypes = {
  userLiked: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired,
  func: PropTypes.func.isRequired,
};

import React from "react";
import PropTypes from "prop-types";

export default function Comments({
  comments,
  val,
  onChange,
  onSubmit,
  onClick,
}) {
  return (
    <div className="cmt-container">
      <div className="comments">
        {comments.map((cmt) => (
          <div className="each-cmt" key={cmt.commentid}>
            <span className="comment-text">
              <a href={cmt.ownerShowUrl}>{cmt.owner}</a> {cmt.text}
            </span>
            {cmt.lognameOwnsThis ? (
              <button
                type="submit"
                className="delete-comment-button"
                onClick={() => onClick(cmt.commentid)}
              >
                Delete comment
              </button>
            ) : null}
          </div>
        ))}
      </div>
      <form className="comment-form" onSubmit={onSubmit}>
        <input
          type="text"
          value={val}
          onChange={(e) => onChange(e.target.value)}
        />
      </form>
    </div>
  );
}

Comments.propTypes = {
  comments: PropTypes.instanceOf(Array).isRequired,
  val: PropTypes.instanceOf(Object).isRequired,
  onChange: PropTypes.instanceOf(Object).isRequired,
  onSubmit: PropTypes.instanceOf(Object).isRequired,
  onClick: PropTypes.instanceOf(Object).isRequired,
};

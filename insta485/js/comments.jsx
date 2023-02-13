import React from "react";

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
        {comments.map((cmt) => {
          return (
            <div className="each-cmt" key={cmt.commentid}>
              <span className="comment-text">
                <a href={cmt.ownerShowUrl}>{cmt.owner}</a> {cmt.text}
              </span>
              {cmt.lognameOwnsThis ? (
                <button
                  className="delete-comment-button"
                  onClick={() => onClick(cmt.commentid)}
                >
                  Delete comment
                </button>
              ) : null}
            </div>
          );
        })}
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

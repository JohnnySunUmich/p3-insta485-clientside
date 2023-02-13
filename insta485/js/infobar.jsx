import React from "react";
import moment from "moment";

export default function InfoBar(args) {
  const { postLink, timeCreated, poster, pfp, posterLink } = args;
  return (
    <div className="header">
      <div className="post-er">
        <div className="pfp">
          <a href={posterLink}>
            <img src={pfp} alt={`${poster}'s pfp`} />
          </a>
        </div>
        <div className="username">
          <a href={posterLink}>{poster}</a>
        </div>
      </div>
      <div className="time-posted">
        <a href={postLink}>{moment.utc(timeCreated).fromNow()}</a>
      </div>
    </div>
  );
}

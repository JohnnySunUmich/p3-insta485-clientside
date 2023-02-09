import React, { useState, useEffect } from "react";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Index() {
    const [render, setRender] = useState(false);
    const [nextUrl, setNextUrl] = useState("");
    const [posts, setPosts] = useState([]);
    const [hasMore, setHasMore] = useState(true);

    useEffect(() => {
        (async () => {
            try {
                let bool = false;
                const response = await fetch("/api/v1/posts/", {credentials: "same-origin"});
                if (!response.ok) throw Error(response.statusText);
                const json = await response.json();
                if (!bool) {
                    setNextUrl(json.next);
                    setPosts(json.results);
                    setRender(true);
                }
                return () => bool = true;
            }
            catch (error) {console.log(error);}
        })();
    }, []);


    const getNextPage = async () => {
        try {
            if (nextUrl !== "") {
                let bool = false;
                const response = await fetch(nextUrl, {credentials: "same-origin"});
                if (!response.ok) throw Error(response.statusText);
                const json = await response.json();
                if (!bool) {
                    setPosts([...posts, ...json.results]);
                    setNextUrl(json.next);
                }
                return () => bool = true;
            }
            else setHasMore(false);
        }
        catch (error) {console.log(error);}
    };

    return (
        render &&
        <InfiniteScroll dataLength={ posts.length } next={ getNextPage } hasMore={ hasMore } loader={ <div>Loading ...</div> }>
            { posts.map(post => <Post url={ post.url } key={ post.postid }/>) }
        </InfiniteScroll>
    );
}
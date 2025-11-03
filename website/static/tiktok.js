import { html } from "rhu/html.js";
import { Style } from "rhu/style.js";
import { BookmarkIcon } from "./icons/bookmark.js";
import { CommentIcon } from "./icons/commenticon.js";
import { HeartIcon } from "./icons/hearticon.js";
import { ShareIcon } from "./icons/share.js";
const style = Style(({ css }) => {
    const wrapper = css.class `
    position: relative;
    width: 100%;
    height: 100%;

    display: flex;
    justify-content: center;
    `;
    const body = css.class `
    width: 100%;
    aspect-ratio: 9 / 16;
    /* border-radius: 25px; */
    background-color: black;
    overflow: hidden;
    `;
    const video = css.class `
    object-fit: contain;
    `;
    const sidebar = css.class `
    position: absolute;
    bottom: 70px;
    right: 0px;
    height: 50%;
    width: 45px;
    margin-right: 20px;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    `;
    const sidebtn = css.class `
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    font-family: tiktok;
    gap: 5px;
    `;
    const pfp = css.class `
    width: 100%;
    height: 100%;
    border-radius: 500px;
    `;
    return {
        wrapper,
        body,
        video,
        sidebar,
        sidebtn,
        pfp
    };
});
export const TikTok = () => {
    let hearts = (Math.ceil(Math.random() * 500) / 10 + 1).toString();
    let comments = (Math.ceil(Math.random() * 500) / 10 + 1).toString();
    let bookmark = (Math.ceil(Math.random() * 500) / 10 + 1).toString();
    let shares = (Math.ceil(Math.random() * 500) / 10 + 1).toString();
    let pic = (Math.floor(Math.random() * 11)).toString();
    const dom = html `
    <div class="${style.wrapper}">
        <div class="${style.body}">
            <video autoplay muted loop class="${style.video}">
                <source src="./videos/${pic}.mp4" type="video/mp4">
            </video>
        </div>
        <div class="${style.sidebar}">
            <div class="${style.sidebtn}" m-id="heart">
                ${HeartIcon()}
                <span>${hearts}k</span>
            </div>
            <div class="${style.sidebtn}" m-id="comment">
                ${CommentIcon()}
                <span>${comments}k</span>
            </div>
            <div class="${style.sidebtn}" m-id="bookmark">
                ${BookmarkIcon()}
                <span>${bookmark}k</span>
            </div>
            <div class="${style.sidebtn}" m-id="share">
                ${ShareIcon()}
                <span>${shares}k</span>
            </div>
            <div class="${style.sidebtn}" style="margin-top: 10px;">
                <img src="./images/pfp/0.png" class="${style.pfp}">
            </div>
        </div>
    </div>
    `;
    html(dom).box();
    dom.share.addEventListener("click", () => {
        fetch("/action/strafeleft", { method: "POST" });
    });
    dom.bookmark.addEventListener("click", () => {
        fetch("/action/straferight", { method: "POST" });
    });
    dom.heart.addEventListener("click", () => {
        fetch("/action/cameraleft", { method: "POST" });
    });
    dom.comment.addEventListener("click", () => {
        fetch("/action/cameraright", { method: "POST" });
    });
    return dom;
};

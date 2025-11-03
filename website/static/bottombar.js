import { html } from "rhu/html.js";
import { Style } from "rhu/style.js";
import { ExploreIcon } from "./icons/exploreicon.js";
import { HomeIcon } from "./icons/homeicon.js";
import { InboxIcon } from "./icons/inboxicon.js";
import { ProfileIcon } from "./icons/profileicon.js";
const style = Style(({ css }) => {
    const wrapper = css.class `
    width: 100%;
    height: 70px;

    background-color: #000000;
    color: white;

    position: fixed;
    bottom: 0px;
    
    display: flex;
    justify-content: center;

    z-index: 1000;
    `;
    const bar = css.class `
    width: 100%;

    display: flex;
    justify-content: center;
    gap: 10px;
    `;
    const btn = css.class `
    height: 100%;
    padding: 10px;
    `;
    return {
        wrapper,
        bar,
        btn
    };
});
export const BottomBar = () => {
    const dom = html `
    <header class="${style.wrapper}">
        <div class="${style.bar}">
            <div class="${style.btn}">${HomeIcon()}</div>
            <div class="${style.btn}">${ExploreIcon()}</div>
            <div style="flex: 1; display: flex; justify-content: center;">
                <img src="./images/upload-icon.png" style="object-fit: contain;">
            </div>
            <div class="${style.btn}" style="padding: 15px;">${InboxIcon()}</div>
            <div class="${style.btn}" style="padding: 15px;">${ProfileIcon()}</div>
        </div>
    </header>
    `;
    html(dom).box();
    return dom;
};

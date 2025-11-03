import { html } from "rhu/html.js";
import { Style } from "rhu/style.js";
import { LiveIcon } from "./icons/live.js";
import { SearchIcon } from "./icons/search.js";
const style = Style(({ css }) => {
    const wrapper = css.class `
    width: 100%;
    height: 70px;

    background-color: #000000;
    color: white;

    position: fixed;
    top: 0px;
    
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
export const Navbar = () => {
    const dom = html `
    <header class="${style.wrapper}">
        <div class="${style.bar}">
            <div class="${style.btn}">${LiveIcon()}</div>
            <div style="flex: 1"></div>
            <div class="${style.btn}" style="padding: 15px;">${SearchIcon()}</div>
        </div>
    </header>
    `;
    html(dom).box();
    return dom;
};

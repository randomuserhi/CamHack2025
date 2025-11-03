import { html } from "rhu/html.js";
import { iconStyle } from "./style.js";
export const ProfileIcon = () => {
    return html `
    <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" class="${iconStyle.wrapper}"><path d="M24 3a10 10 0 1 1 0 20 10 10 0 0 1 0-20Zm0 4a6 6 0 1 0 0 12.00A6 6 0 0 0 24 7Zm0 19c10.3 0 16.67 6.99 17 17 .02.55-.43 1-1 1h-2c-.54 0-.98-.45-1-1-.3-7.84-4.9-13-13-13s-12.7 5.16-13 13c-.02.55-.46 1-1.02 1h-2c-.55 0-1-.45-.98-1 .33-10.01 6.7-17 17-17Z"></path></svg>
    `;
};

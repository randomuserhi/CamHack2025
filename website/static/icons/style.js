import { Style } from "rhu/style.js";
export const iconStyle = Style(({ css }) => {
    const wrapper = css.class `
    width: 100%;
    height: 100%;
    `;
    return {
        wrapper
    };
});

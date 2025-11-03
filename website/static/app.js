import { html } from "rhu/html.js";
import { Style } from "rhu/style.js";
import { BottomBar } from "./bottombar.js";
import { Navbar } from "./navbar.js";
import { TikTok } from "./tiktok.js";
const style = Style(({ css }) => {
    const wrapper = css.class `
    width: 100%;
    flex: 1;

    position: relative;

    display: flex;
    justify-content: center;

    background-color: black;
    `;
    const body = css.class `
    position: relative;
    aspect-ratio: 9 / 16;
    height: 100%;
    `;
    return {
        wrapper,
        body
    };
});
const App = () => {
    const dom = html `
    ${Navbar()}
    ${BottomBar()}
    <div class="${style.wrapper}">
        <div m-id="body" class="${style.body}">
            ${TikTok()}
            ${TikTok()}
            ${TikTok()}
            ${TikTok()}
            ${TikTok()}
            ${TikTok()}
        </div>
    </div>
    `;
    html(dom).box();
    let index = 0;
    window.addEventListener("scrollend", () => {
        const scrollTop = window.scrollY;
        const current = dom.body.children[index];
        const rect = current.getBoundingClientRect();
        if (scrollTop > current.offsetTop + rect.height / 4) {
            index++;
            fetch(`/action/forward`, { method: 'POST' });
            if (index >= dom.body.children.length - 5) {
                for (let i = 0; i < 10; ++i) {
                    dom.body.append(...TikTok());
                }
            }
        }
        else if (scrollTop < current.offsetTop - rect.height / 4) {
            index--;
            fetch(`/action/backward`, { method: 'POST' });
        }
        window.scrollTo({
            top: dom.body.children[index].offsetTop,
            behavior: 'smooth'
        });
    });
    return dom;
};
export const app = App();
const __load__ = () => {
    document.body.replaceChildren(...app);
    const SWIPE_THRESHOLD = 30;
    const MAX_TAP_MOVEMENT = 10;
    const MAX_TAP_DURATION = 250;
    const DOUBLE_TAP_DELAY = 300;
    const DOUBLE_TAP_MAX_DISTANCE = 40;
    let onSwipe = (direction, ev) => {
        let action = {
            "up": "forward",
            "down": "backward"
        }[direction];
        if (action) {
            fetch(`/action/${action}`, { method: 'POST' });
        }
    };
    let onTap = (info) => {
        fetch(`/action/interact`, { method: 'POST' });
    };
    let onDoubleTap = (info) => {
        fetch(`/action/shoot`, { method: 'POST' });
    };
    let activeId = null;
    let startX = 0;
    let startY = 0;
    let startTime = 0;
    let moved = false;
    let swipeDetected = false;
    let lastTapTime = 0;
    let lastTapX = 0;
    let lastTapY = 0;
    let singleTapTimer = null;
    function distance(aX, aY, bX, bY) {
        const dx = aX - bX;
        const dy = aY - bY;
        return Math.hypot(dx, dy);
    }
    function detectSwipeIfNeeded(x, y, ev) {
    }
    function handleTap(x, y, time, sourceEvent) {
        const now = time;
        const sinceLast = now - lastTapTime;
        if (sinceLast > 0 && sinceLast <= DOUBLE_TAP_DELAY &&
            distance(x, y, lastTapX, lastTapY) <= DOUBLE_TAP_MAX_DISTANCE) {
            if (singleTapTimer) {
                clearTimeout(singleTapTimer);
                singleTapTimer = null;
            }
            lastTapTime = 0;
            lastTapX = 0;
            lastTapY = 0;
            onDoubleTap({ x, y, time: now, sourceEvent });
            return;
        }
        lastTapTime = now;
        lastTapX = x;
        lastTapY = y;
        if (singleTapTimer)
            clearTimeout(singleTapTimer);
        singleTapTimer = setTimeout(() => {
            singleTapTimer = null;
            lastTapTime = 0;
            onTap({ x, y, time: now, sourceEvent });
        }, DOUBLE_TAP_DELAY);
    }
    function resetState() {
        activeId = null;
        startX = 0;
        startY = 0;
        startTime = 0;
        moved = false;
        swipeDetected = false;
    }
    document.addEventListener('pointerdown', (e) => {
        if (!e.isPrimary)
            return;
        activeId = e.pointerId;
        startX = e.clientX;
        startY = e.clientY;
        startTime = e.timeStamp || Date.now();
        moved = false;
        swipeDetected = false;
    }, { passive: true });
    document.addEventListener('pointermove', (e) => {
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        if (Math.abs(dx) > MAX_TAP_MOVEMENT || Math.abs(dy) > MAX_TAP_MOVEMENT) {
            moved = true;
        }
        detectSwipeIfNeeded(e.clientX, e.clientY, e);
    }, { passive: true });
    document.addEventListener('pointerup', (e) => {
        if (swipeDetected) {
            resetState();
            return;
        }
        const endTime = e.timeStamp || Date.now();
        const duration = endTime - startTime;
        if (!moved && duration <= MAX_TAP_DURATION) {
            handleTap(e.clientX, e.clientY, endTime, e);
        }
        resetState();
    });
    document.addEventListener('pointercancel', () => resetState());
};
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", __load__);
}
else {
    __load__();
}

# Recipes

Code for the rules in `../SKILL.md`, plus techniques too specific for every invocation.

## Components

### Press feedback

```css
.button {
  transition: transform 160ms ease-out;
}

.button:active {
  transform: scale(0.97);
}
```

`scale()` also scales the element's children, so the label and icon shrink with the button.

### Entrance without scale(0)

```css
.entering {
  transform: scale(0.95);
  opacity: 0;
}
```

### Tooltips that skip the delay

```css
.tooltip {
  transition: transform 125ms ease-out, opacity 125ms ease-out;
  transform-origin: var(--transform-origin);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

### Interruptible toasts

Use a transition, not a keyframe animation, so a toast added mid-animation retargets instead of restarting.

```css
.toast {
  transition: transform 400ms ease;
}
```

### Enter states with @starting-style

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

This replaces setting a `mounted` flag in an effect after the first render. Where browser support falls short, fall back to that pattern.

```jsx
useEffect(() => {
  setMounted(true);
}, []);
// <div data-mounted={mounted}>
```

### Blur over a crossfade

```css
.button-content {
  transition: filter 200ms ease, opacity 200ms ease;
}

.button-content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Without blur the eye sees the old and new states as two objects. Blur blends them into one change.

### Stagger

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms ease-out forwards;
}

.item:nth-child(2) {
  animation-delay: 50ms;
}
.item:nth-child(3) {
  animation-delay: 100ms;
}
.item:nth-child(4) {
  animation-delay: 150ms;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### List items that enter and exit

When an item's opacity and height animate together, as in Family's drawer, no formula makes them line up. Adjust both until they look right in slow motion.

## Springs

Motion takes a duration and bounce, which is easier to reason about, or physical parameters for more control.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

### Mouse tracking

Tying a value straight to the cursor looks mechanical. Run it through `useSpring` so it trails with momentum.

```jsx
import { useMotionValue, useSpring, useTransform } from 'framer-motion';

const mouseX = useMotionValue(0);
const rotation = useTransform(mouseX, (x) => x * 0.1);
const springRotation = useSpring(rotation, { stiffness: 100, damping: 10 });
// <motion.div style={{ rotate: springRotation }} onMouseMove={(e) => mouseX.set(e.clientX)} />
```

Use this only for decoration. A functional chart in a banking app should track the cursor exactly.

## Transforms

### Percentage translate

A percentage in `translate()` is relative to the element's own size, so `translateY(100%)` moves an element by its own height at any size. Sonner positions toasts this way and Vaul hides its drawer this way. Prefer it to hardcoded pixels.

```css
.drawer-hidden {
  transform: translateY(100%);
}

.toast-enter {
  transform: translateY(-100%);
}
```

### 3D depth

`rotateX()` and `rotateY()` under `transform-style: preserve-3d` give real depth for orbits, coin flips, and other depth effects without JavaScript.

```css
.wrapper {
  transform-style: preserve-3d;
}

@keyframes orbit {
  from {
    transform: translate(-50%, -50%) rotateY(0deg) translateZ(72px) rotateY(360deg);
  }
  to {
    transform: translate(-50%, -50%) rotateY(360deg) translateZ(72px) rotateY(0deg);
  }
}
```

## clip-path

`clip-path: inset(top right bottom left)` clips a rectangle, and each value cuts in from its side.

### Hold to delete

Put a colored overlay on the button, clipped fully from the right. Fill it slowly on press and snap it back on release. Add press feedback to the button itself.

```css
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms ease-out;
}

.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;
}
```

### Tabs with exact color transitions

Duplicate the tab list and style the copy as active, with its own background and text color. Clip the copy so only the active tab shows, and animate the clip when the tab changes. The colors change exactly at the moving edge, which separate color transitions can't match.

### Image reveal on scroll

Start at `clip-path: inset(0 0 100% 0)` and animate to `inset(0 0 0 0)` when the image enters the viewport. Detect entry with `IntersectionObserver`, or Motion's `useInView` with `{ once: true, margin: "-100px" }`.

### Comparison slider

Stack two images and clip the top one with `clip-path: inset(0 50% 0 0)`. Set the right inset from the drag position. It needs no extra DOM elements and runs hardware-accelerated.

## Gestures

### Dismiss on velocity

Don't require a drag past a threshold. A quick flick should dismiss.

```js
const velocity = Math.abs(swipeAmount) / (Date.now() - dragStartTime);

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

### Friction past a boundary

When the user drags past a limit, like a drawer already fully open, let the element follow with growing resistance instead of stopping it dead. The further they drag, the less it moves.

### Pointer capture

Capture the pointer when a drag starts so the drag continues after the pointer leaves the element.

```js
element.setPointerCapture(event.pointerId);
```

### One pointer per drag

Ignore new touch points once a drag starts. Otherwise a finger switch mid-drag makes the element jump.

```js
function onPress() {
  if (isDragging) return;
  // start the drag
}
```

## Performance

### Transform on the element, not a variable on the parent

```js
// Recalculates styles for every child
element.style.setProperty('--swipe-amount', `${distance}px`);

element.style.transform = `translateY(${distance}px)`;
```

### Hardware-accelerated Motion

```jsx
// Runs on requestAnimationFrame and drops frames under load
<motion.div animate={{ x: 100 }} />

<motion.div animate={{ transform: "translateX(100px)" }} />
```

The Vercel dashboard's tab animation used Motion's shared layout animations and dropped frames during page loads. Moving it to CSS animations fixed it.

### Web Animations API

WAAPI gives JavaScript control with CSS performance, interrupts cleanly, and needs no library.

```js
element.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }], {
  duration: 1000,
  fill: 'forwards',
  easing: 'cubic-bezier(0.77, 0, 0.175, 1)',
});
```

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: fade 0.2s ease;
  }
}

@media (hover: hover) and (pointer: fine) {
  .element:hover {
    transform: scale(1.05);
  }
}
```

```jsx
const shouldReduceMotion = useReducedMotion();
const closedX = shouldReduceMotion ? 0 : '-100%';
```

## Testing on a phone

Connect the phone over USB, open the local dev server by the machine's IP address, and inspect with Safari's remote devtools. A simulator works for layout but not for how a gesture feels.

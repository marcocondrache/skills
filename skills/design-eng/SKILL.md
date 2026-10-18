---
name: design-eng
description: "Build or review UI motion and interaction details so an interface feels right. Use for /design-eng, 'review this animation', 'make this feel better', 'polish this UI', 'what easing should this use', or building a popover, toast, drawer, tooltip, or button with motion."
disable-model-invocation: true
---

# Design engineering

Users rarely notice a single detail like an easing curve, a transform origin, or a skipped tooltip delay. They notice when many of them are wrong. Get each one right.

Run the decision steps before you write any animation. Apply the rules to every component you touch. Load `references/recipes.md` for the code behind a rule, or for clip-path, 3D transforms, springs, and drag gestures.

## Decide before you animate

Answer these in order.

### 1. Should it animate at all

Ask how often a user sees it.

| Frequency | Decision |
| --- | --- |
| 100+ times a day (keyboard shortcuts, command palette toggle) | No animation |
| Tens of times a day (hover effects, list navigation) | Remove it or cut it down |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare or first-time (onboarding, feedback forms, celebrations) | Room for delight |

Never animate an action the keyboard starts. Raycast has no open or close animation, which is right for something opened hundreds of times a day.

### 2. What is it for

Name the reason before you write it. These are the valid ones.

- **Spatial consistency.** A toast enters and exits from the same side, so swipe to dismiss is obvious.
- **State.** A button morphs to show that its state changed.
- **Explanation.** A marketing animation shows how a feature works.
- **Feedback.** A button scales down on press to confirm the input.
- **Continuity.** An element that appears or disappears with no transition looks broken.

If the only reason is that it looks good and users see it often, don't animate it.

### 3. Which easing

| Motion | Easing |
| --- | --- |
| Entering or exiting | ease-out |
| Moving or morphing on screen | ease-in-out |
| Hover or color change | ease |
| Constant motion (marquee, progress bar) | linear |
| Anything else | ease-out |

Use custom curves, because the built-in CSS keywords are too weak.

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
/* iOS-like drawer curve from Ionic */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

Never use ease-in on UI. It delays the first movement, which is the moment the user watches most, so a 300ms ease-in dropdown feels slower than a 300ms ease-out one. Find stronger variants of the standard curves at [easing.dev](https://easing.dev/) or [easings.co](https://easings.co/) instead of inventing one.

### 4. How long

| Element | Duration |
| --- | --- |
| Button press feedback | 100-160ms |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects | 150-250ms |
| Modals, drawers | 200-500ms |
| Marketing, explanatory | Longer is fine |

Keep every other UI animation under 300ms. Duration changes how fast the app seems. A 180ms select feels more responsive than a 400ms one, and a faster spinner makes the same load feel shorter.

## Rules

- **Press feedback.** Give every pressable element `transform: scale(0.97)` on `:active` with a 160ms ease-out transition. Keep the scale between 0.95 and 0.98.
- **No scale(0).** Start an entrance at `scale(0.95)` or higher, with `opacity: 0`. An element that grows from `scale(0)` looks like it came from nowhere.
- **Origin-aware popovers.** Scale a popover from its trigger with `transform-origin: var(--transform-origin)`, which Base UI sets. Modals keep `transform-origin: center`, because no trigger anchors them.
- **Tooltip delay once.** Delay the first tooltip so a passing cursor doesn't open it. Once one is open, open its neighbors instantly with no animation.
- **Transitions over keyframes.** Use CSS transitions for anything triggered in quick succession, like toasts and toggles. An interrupted transition retargets from its current value. A keyframe animation restarts from zero.
- **Springs for gestures.** Use a spring for a drag with momentum, a gesture the user may reverse halfway, or an element that should feel alive, like the Dynamic Island. A spring keeps its velocity when interrupted. Keep bounce between 0.1 and 0.3, and leave it out of most UI.
- **Blur for crossfades.** When a crossfade still shows two overlapping objects after you tune easing and duration, add `filter: blur(2px)` during the transition. Keep blur under 20px, because heavy blur is expensive in Safari.
- **Asymmetric timing.** Go slow where the user decides and fast where the system responds. A hold-to-delete fills over 2s linear and snaps back in 200ms ease-out.
- **Stagger.** When several elements enter together, delay each by 30-80ms after the last. Never block input while a stagger plays.
- **Motion matches the component.** A playful component can bounce. A dashboard should be crisp and fast. Sonner runs slightly slower than typical UI and uses `ease` instead of ease-out to feel calmer.
- **Unseen edge cases.** Handle the cases a user would notice only if they broke. Pause toast timers while the tab is hidden. Fill the gaps between stacked toasts with a pseudo-element so hover holds. Capture the pointer during a drag.
- **Defaults over options.** Ship excellent default easing, timing, and visuals, because most users never customize them. Keep a component's setup to one mount point and one function call, like Sonner's `<Toaster />` and `toast()`.

## Performance

- Animate only `transform` and `opacity`. Animating `width`, `height`, `padding`, or `margin` runs layout and paint on every frame.
- Don't drive per-frame motion through a CSS variable on a parent. Each change recalculates styles for every child. Set `transform` on the moving element instead.
- Use CSS animations or the Web Animations API for motion you can define up front. They run off the main thread and stay smooth while the page loads. Keep JS-driven animation for motion that follows input.
- In Motion (formerly Framer Motion), `x`, `y`, and `scale` run on `requestAnimationFrame` and drop frames under load. Animate a full `transform` string to get hardware acceleration.

## Accessibility

- Under `prefers-reduced-motion: reduce`, remove movement and position changes, and keep the opacity and color transitions that help the user follow a change. Reduced motion means fewer and gentler animations, not none.
- Gate hover animation behind `@media (hover: hover) and (pointer: fine)`, because touch devices fire hover on tap.

## Verify

Slow the animation to 2-5x its duration, or step through it frame by frame in the browser devtools animations panel. Check that colors blend instead of showing two states at once, that it doesn't start or stop abruptly, that it scales from the right origin, and that opacity, transform, and color stay in sync. Test drags and swipes on a physical device, and say so when you couldn't.

## Review

Report findings as one markdown table with Before, After, and Why columns, one row per issue. Never write Before and After on separate lines.

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Name the properties instead of `all` |
| `ease-in` on a dropdown | `ease-out` with a custom curve | ease-in delays the first movement |

Check for these.

| Issue | Fix |
| --- | --- |
| `transition: all` | Name the properties, like `transition: transform 200ms ease-out` |
| An entrance from `scale(0)` | Start at `scale(0.95)` with `opacity: 0` |
| `ease-in` on UI | ease-out or a custom curve |
| `transform-origin: center` on a popover | The trigger's position or `var(--transform-origin)`. Modals stay centered |
| Animation on a keyboard action | Remove it |
| A UI animation over 300ms | 150-250ms, or up to 500ms for a modal or drawer |
| A hover animation with no media query | `@media (hover: hover) and (pointer: fine)` |
| Keyframes on an element triggered in quick succession | A CSS transition |
| Motion `x` or `y` under load | `transform: "translateX(...)"` |
| A release as slow as the press | A fast release, like a 2s press and a 200ms release |
| Elements that enter all at once | A 30-80ms stagger |

# Accessibility Primitives

The frontend has a lot of interactive surfaces — the command palette, dialogs,
dropdowns, the notification centre, the sidebar — and no shared accessibility
building blocks. So each one re-solves the same problems, slightly differently
and slightly wrong.

This is the shared layer. No new dependency; a few hundred lines of DOM code
with tests.

## What was broken

* **No skip link.** A keyboard user landing on any page had to tab through the
  entire sidebar and header before reaching the content. On the dashboard that
  is roughly forty stops, on *every single navigation*.
* **Nothing trapped focus in a modal.** Tab enough times in a dialog and focus
  walks into the page behind it — still there, still focusable, covered by an
  overlay. The user is now typing into something they cannot see.
* **Focus was never restored.** Closing a dialog dropped focus to `<body>`, so
  the next Tab started from the top of the document instead of the button just
  used.
* **Nothing was announced.** Toasts, "saved", "3 new notifications", search
  result counts — invisible to a screen reader, because there was no live
  region. `aria-live` appeared in three files, each hand-rolled.
* **Composite widgets were N tab stops.** A toolbar should be one stop with
  arrow-key navigation between items.

## `lib/a11y/tabbable.ts`

The primitive everything else is built on, and the fiddly part.

`container.querySelectorAll("button, a[href], input, …")` gets the common case
right and then goes wrong on:

* a `disabled` button — **and** one inside a `disabled` fieldset, except
  anything inside that fieldset's first `<legend>`, which stays interactive
* anything inside an `inert` subtree
* `display: none` / `visibility: hidden` / `hidden`
* collapsed `<details>` content, while keeping its `<summary>`
* `tabindex="-1"` — focusable by script, skipped by Tab
* **radio groups**, which are *one* tab stop: the checked member, or the first
  if none is checked. Treating each as its own stop makes a focus trap loop
  through a form's radio options one at a time.
* **positive `tabindex`**, which the browser visits *before* everything in
  document order

That last one is the most commonly missed. A trap that ignores it wraps in a
different order than Tab does, and the user ends up somewhere they did not
expect.

```ts
import { getTabbableElements, getTabbableEdges, focusFirst } from "@/lib/a11y";
```

`focusFirst` falls back to focusing the container itself when nothing inside is
tabbable — focus has to land *somewhere* inside a dialog, or a screen reader
stays on the page behind it.

## `useFocusTrap`

```tsx
const ref = useFocusTrap<HTMLDivElement>({
  active: open,
  onEscape: () => setOpen(false),
});

return <div ref={ref} role="dialog">…</div>;
```

Two details that a minimal version gets wrong:

**Edges are recomputed on every keypress**, not cached when the trap opens.
Dialog content changes — a validation error appears, a disclosure expands, a
button becomes enabled — and a cached "last element" sends focus to something
that is no longer there.

**Focus is pulled back when it has escaped.** The user can click something
behind the overlay, or a script can move focus. If the trap only handles the
wrap case, that situation is unrecoverable by keyboard.

Focus is restored to the previously focused element on release, and the hook
checks the element is still in the document first — it may have been removed
while the dialog was open.

## `useRovingTabIndex`

Makes a group of controls a single tab stop, with arrow keys moving inside it.
The WAI-ARIA authoring-practices pattern: exactly one item carries
`tabIndex={0}`, the rest carry `-1`, and the index moves as the user arrows
around.

```tsx
const { containerRef, getItemProps, containerProps } = useRovingTabIndex({
  orientation: "horizontal",
});

<div ref={containerRef} role="toolbar" {...containerProps}>
  {items.map((item, i) => (
    <button key={item.id} {...getItemProps(i)}>{item.label}</button>
  ))}
</div>
```

| Option | Default | |
| --- | --- | --- |
| `orientation` | `"horizontal"` | `"vertical"` or `"both"` |
| `loop` | `true` | Wrap at the ends |
| `typeahead` | `false` | Jump by typing a label's first letters |

`getItemProps` includes an `onFocus` handler, and it matters as much as the
keyboard handling: somebody can click or shift-tab straight into the middle of
the group, and if the index does not follow, the next arrow press jumps back to
wherever the index was left.

A horizontal group deliberately ignores `ArrowUp`/`ArrowDown` — the page still
needs to scroll.

## The announcer

```tsx
const { announce } = useAnnouncer();

announce("Project saved");                    // polite
announce("Upload failed", "assertive");       // interrupts
```

`AnnouncerProvider` is mounted once in `__root.tsx` and renders two live
regions. **Two, not one**, because `aria-live` is read when the region is first
seen — flipping the attribute on an existing region does nothing on most screen
readers.

Use `polite` for anything the user can catch up on. Reserve `assertive` for
errors that block what they were doing.

### The zero-width space

Screen readers only re-announce a live region when its **text changes**.
Announcing "3 results", then "3 results" again after a different search,
produces *silence* the second time — and the user concludes nothing happened.

Appending U+200B makes the text technically different while being inaudible and
invisible. It is the standard workaround, and it is the kind of thing every
hand-rolled live region rediscovers the hard way.

The regions are clipped, not `hidden` and not `display: none` — either of those
removes them from the accessibility tree, which is exactly the opposite of what
they are for.

`useAnnouncer` falls back to a no-op outside a provider, so a component using it
still works in isolation and in tests that do not care.

## `SkipLink`

Mounted first in `__root.tsx`, so it is the first thing in the tab order.
Target is `#main-content` on the `<main>` in `DashboardLayout`.

A bare `href="#main-content"` moves the **scroll position but not focus**
unless the target is focusable — so the next Tab starts from the top of the
document again and the user is back where they began. The link therefore sets
`tabindex="-1"` on the target and focuses it explicitly.

## `useFocusVisible`

Whether the user is currently navigating by keyboard. Prefer the
`:focus-visible` CSS pseudo-class where it works; this is for cases CSS cannot
reach — deciding whether to *render* an affordance, whether to scroll a newly
focused item into view, whether to open a menu on focus.

## Notes

* **Everything is SSR-safe.** This app server-renders; nothing here touches
  `document` at module scope, and `useFocusVisible` guards for it.
* **No new runtime dependency.**
* 61 tests, covering each exclusion rule in `tabbable` individually.

## If you are building a menu

Use these. The point of the layer is that there is not a sixth hand-rolled
focus trap in the codebase.

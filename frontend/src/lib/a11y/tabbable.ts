/**
 * Finding the elements a keyboard user can actually reach.
 *
 * This is the primitive everything else in `lib/a11y` is built on, and it is
 * the part that is genuinely fiddly. A naive
 * `container.querySelectorAll("button, a[href], input, …")` gets the common
 * case right and then goes wrong on all of these:
 *
 * - a `disabled` button, or one inside a `disabled` fieldset
 * - anything inside an `inert` subtree
 * - `display: none` / `visibility: hidden` / `hidden`
 * - collapsed `<details>` content
 * - `tabindex="-1"`, which is focusable but not *tabbable*
 * - radio buttons: only the checked member of a group is a tab stop, and if
 *   none is checked, only the first
 * - positive `tabindex`, which the browser visits *before* everything in
 *   document order
 *
 * That last one is the most commonly missed. A focus trap that ignores
 * positive tabindex wraps in a different order than Tab does, and the user
 * ends up somewhere they did not expect.
 *
 * Everything here is SSR-safe: nothing touches `document` at module scope.
 */

/**
 * Elements that are focusable by default, plus anything given an explicit
 * `tabindex`. Kept as a single selector so the DOM is only walked once.
 */
const FOCUSABLE_SELECTOR = [
  "a[href]",
  "area[href]",
  "button",
  "input",
  "select",
  "textarea",
  "details > summary:first-of-type",
  "iframe",
  "object",
  "embed",
  "audio[controls]",
  "video[controls]",
  "[contenteditable]:not([contenteditable='false'])",
  "[tabindex]",
].join(",");

function isDisabled(element: Element): boolean {
  if ((element as HTMLInputElement).disabled) return true;

  // A disabled fieldset disables its descendants -- except anything inside
  // its first <legend>, which stays interactive. That exception is real and
  // people do use it for a "customise" toggle above a disabled block.
  const fieldset = element.closest("fieldset[disabled]");
  if (!fieldset) return false;

  const legend = fieldset.querySelector(":scope > legend");
  return !legend || !legend.contains(element);
}

function isInert(element: Element): boolean {
  // `inert` removes a whole subtree from the accessibility tree and from tab
  // order. It is how a correctly built modal turns off the page behind it.
  return element.closest("[inert]") !== null;
}

function isHiddenByAttribute(element: Element): boolean {
  return element.closest("[hidden]") !== null;
}

function isInsideClosedDetails(element: Element): boolean {
  const details = element.closest("details:not([open])");
  if (!details) return false;

  // The summary of a closed <details> is still a tab stop; everything after
  // it is not.
  const summary = details.querySelector(":scope > summary");
  return !summary || !summary.contains(element);
}

function isRendered(element: HTMLElement): boolean {
  // Computed style rather than offsetParent: offsetParent is null for
  // position:fixed elements too, which are perfectly visible.
  //
  // Deliberately no bounding-rect check. It would catch an element collapsed
  // to zero size, but jsdom lays nothing out, so every rect is 0×0 there and
  // the whole tab order would come back empty under test.
  const style = element.ownerDocument.defaultView?.getComputedStyle(element);
  if (!style) return true;

  if (style.display === "none" || style.visibility === "hidden") return false;
  if (style.contentVisibility === "hidden") return false;

  return true;
}

/**
 * Radio buttons form a group, and the group is one tab stop.
 *
 * The checked radio is the stop. If none is checked, the first one is. Any
 * other member is focusable with an arrow key but is not reached by Tab, and
 * treating each as its own stop makes a focus trap loop through a form's radio
 * options one at a time.
 */
function isNonTabbableRadio(element: HTMLInputElement): boolean {
  if (element.type !== "radio") return false;
  if (element.checked) return false;

  const root = element.form ?? element.ownerDocument;
  const name = element.name;

  if (!name) return false;

  const group = Array.from(
    root.querySelectorAll<HTMLInputElement>(`input[type="radio"][name="${CSS.escape(name)}"]`),
  );

  const checked = group.find((radio) => radio.checked);
  if (checked) return true;

  return group[0] !== element;
}

/** Whether an element can receive focus programmatically. */
export function isFocusable(element: HTMLElement): boolean {
  if (isDisabled(element)) return false;
  if (isInert(element)) return false;
  if (isHiddenByAttribute(element)) return false;
  if (isInsideClosedDetails(element)) return false;
  if (!isRendered(element)) return false;

  return true;
}

/**
 * Whether a contenteditable host is tabbable.
 *
 * Browsers report `tabIndex === 0` for these, but not every DOM
 * implementation does -- jsdom reports -1, because its `tabIndex` getter only
 * knows about the elements on its focusable-areas list. Reading the attribute
 * is the portable answer, and an explicit `tabindex` still wins.
 */
function isEditableHost(element: HTMLElement): boolean {
  const value = element.getAttribute("contenteditable");
  if (value === null || value === "false") return false;

  return !element.hasAttribute("tabindex");
}

/** Whether Tab will stop on an element. */
export function isTabbable(element: HTMLElement): boolean {
  if (!isFocusable(element)) return false;

  // tabindex="-1" is the difference between focusable and tabbable: reachable
  // by script, skipped by Tab.
  if (element.tabIndex < 0 && !isEditableHost(element)) return false;

  if (element instanceof HTMLInputElement && isNonTabbableRadio(element)) {
    return false;
  }

  return true;
}

/**
 * Every tabbable descendant of `container`, in the order Tab visits them.
 *
 * Positive `tabindex` values come first, ascending, then everything with
 * `tabindex="0"` or an implicit stop in document order. That is what the
 * browser does, and a trap that sorts differently sends focus somewhere the
 * user is not expecting.
 */
export function getTabbableElements(container: HTMLElement | null): HTMLElement[] {
  if (!container) return [];

  const candidates = Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
    isTabbable,
  );

  // The container itself can be a stop, and often is -- a dialog with
  // tabindex="-1" is not, but one with tabindex="0" is.
  if (isTabbable(container)) {
    candidates.unshift(container);
  }

  const positive: { element: HTMLElement; index: number; order: number }[] = [];
  const natural: HTMLElement[] = [];

  candidates.forEach((element, order) => {
    if (element.tabIndex > 0) {
      positive.push({ element, index: element.tabIndex, order });
    } else {
      natural.push(element);
    }
  });

  // Ties within the same positive tabindex resolve by document order, which
  // is why the original index is carried along.
  positive.sort((a, b) => a.index - b.index || a.order - b.order);

  return [...positive.map((entry) => entry.element), ...natural];
}

/** The first and last tab stops in a container, or `null` if there are none. */
export function getTabbableEdges(
  container: HTMLElement | null,
): { first: HTMLElement; last: HTMLElement } | null {
  const elements = getTabbableElements(container);
  if (elements.length === 0) return null;

  return { first: elements[0], last: elements[elements.length - 1] };
}

/**
 * Move focus to the first tab stop in a container.
 *
 * Falls back to the container itself, which is what a dialog with no
 * interactive content needs -- focus has to land *somewhere* inside, or the
 * screen reader stays on the page behind.
 */
export function focusFirst(container: HTMLElement | null): boolean {
  if (!container) return false;

  const elements = getTabbableElements(container);

  if (elements.length > 0) {
    elements[0].focus();
    return true;
  }

  if (container.tabIndex < 0) {
    container.setAttribute("tabindex", "-1");
  }
  container.focus();
  return false;
}

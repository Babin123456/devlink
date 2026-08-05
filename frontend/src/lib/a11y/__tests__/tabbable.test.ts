import { afterEach, describe, expect, it } from "vitest";

import { focusFirst, getTabbableEdges, getTabbableElements, isTabbable } from "../tabbable";

function mount(html: string): HTMLElement {
  const container = document.createElement("div");
  container.innerHTML = html;
  document.body.appendChild(container);
  return container;
}

afterEach(() => {
  document.body.innerHTML = "";
});

describe("getTabbableElements", () => {
  it("finds the ordinary focusable elements in document order", () => {
    const container = mount(`
      <a href="/a">link</a>
      <button>button</button>
      <input />
      <select></select>
      <textarea></textarea>
    `);

    expect(getTabbableElements(container).map((el) => el.tagName)).toEqual([
      "A",
      "BUTTON",
      "INPUT",
      "SELECT",
      "TEXTAREA",
    ]);
  });

  it("skips an anchor with no href", () => {
    // <a> without href is not a link and the browser does not stop on it.
    const container = mount(`<a>not a link</a><button>real</button>`);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips disabled controls", () => {
    const container = mount(`<button disabled>no</button><button>yes</button>`);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips controls inside a disabled fieldset", () => {
    const container = mount(`
      <fieldset disabled><button>no</button></fieldset>
      <button>yes</button>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("keeps controls inside a disabled fieldset's first legend", () => {
    // A real exception in the HTML spec, and people use it for a "customise"
    // toggle sitting above a disabled block.
    const container = mount(`
      <fieldset disabled>
        <legend><button>still on</button></legend>
        <button>off</button>
      </fieldset>
    `);

    const tabbable = getTabbableElements(container);

    expect(tabbable).toHaveLength(1);
    expect(tabbable[0].textContent).toBe("still on");
  });

  it("skips anything inside an inert subtree", () => {
    // inert is how a correctly built modal turns off the page behind it.
    const container = mount(`
      <div inert><button>behind the modal</button></div>
      <button>in the modal</button>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips anything inside a hidden subtree", () => {
    const container = mount(`
      <div hidden><button>no</button></div>
      <button>yes</button>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips display:none", () => {
    const container = mount(`
      <button style="display: none">no</button>
      <button>yes</button>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips visibility:hidden", () => {
    const container = mount(`
      <button style="visibility: hidden">no</button>
      <button>yes</button>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("skips tabindex=-1", () => {
    // Focusable by script, not reachable by Tab. That distinction is the
    // whole difference between isFocusable and isTabbable.
    const container = mount(`<button tabindex="-1">no</button><button>yes</button>`);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("visits positive tabindex before document order", () => {
    // The most commonly missed rule. A trap that ignores it wraps in a
    // different order than Tab does.
    const container = mount(`
      <button id="natural">natural</button>
      <button id="third" tabindex="3">third</button>
      <button id="first" tabindex="1">first</button>
    `);

    expect(getTabbableElements(container).map((el) => el.id)).toEqual([
      "first",
      "third",
      "natural",
    ]);
  });

  it("breaks ties in positive tabindex by document order", () => {
    const container = mount(`
      <button id="a" tabindex="2">a</button>
      <button id="b" tabindex="2">b</button>
    `);

    expect(getTabbableElements(container).map((el) => el.id)).toEqual(["a", "b"]);
  });

  it("treats a radio group as a single tab stop", () => {
    // Otherwise a focus trap loops through a form's radio options one at a
    // time, which is not how the browser behaves.
    const container = mount(`
      <input type="radio" name="plan" id="r1" />
      <input type="radio" name="plan" id="r2" checked />
      <input type="radio" name="plan" id="r3" />
    `);

    const tabbable = getTabbableElements(container);

    expect(tabbable).toHaveLength(1);
    expect(tabbable[0].id).toBe("r2");
  });

  it("uses the first radio when none is checked", () => {
    const container = mount(`
      <input type="radio" name="plan" id="r1" />
      <input type="radio" name="plan" id="r2" />
    `);

    expect(getTabbableElements(container)[0].id).toBe("r1");
  });

  it("keeps radios in different groups separate", () => {
    const container = mount(`
      <input type="radio" name="a" id="a1" />
      <input type="radio" name="b" id="b1" />
    `);

    expect(getTabbableElements(container)).toHaveLength(2);
  });

  it("skips the content of a closed details but keeps its summary", () => {
    const container = mount(`
      <details>
        <summary>toggle</summary>
        <button>hidden until open</button>
      </details>
    `);

    const tabbable = getTabbableElements(container);

    expect(tabbable).toHaveLength(1);
    expect(tabbable[0].tagName).toBe("SUMMARY");
  });

  it("includes the content of an open details", () => {
    const container = mount(`
      <details open>
        <summary>toggle</summary>
        <button>now reachable</button>
      </details>
    `);

    expect(getTabbableElements(container)).toHaveLength(2);
  });

  it("includes contenteditable but not contenteditable=false", () => {
    const container = mount(`
      <div contenteditable="true">yes</div>
      <div contenteditable="false">no</div>
    `);

    expect(getTabbableElements(container)).toHaveLength(1);
  });

  it("returns an empty list for a null container", () => {
    expect(getTabbableElements(null)).toEqual([]);
  });

  it("returns an empty list when nothing is tabbable", () => {
    expect(getTabbableElements(mount(`<p>just text</p>`))).toEqual([]);
  });
});

describe("isTabbable", () => {
  it("distinguishes focusable from tabbable", () => {
    const container = mount(`<button tabindex="-1">focusable only</button>`);
    const button = container.querySelector("button")!;

    expect(isTabbable(button)).toBe(false);
  });
});

describe("getTabbableEdges", () => {
  it("returns the first and last stops", () => {
    const container = mount(`
      <button id="a">a</button>
      <button id="b">b</button>
      <button id="c">c</button>
    `);

    const edges = getTabbableEdges(container)!;

    expect(edges.first.id).toBe("a");
    expect(edges.last.id).toBe("c");
  });

  it("returns the same element for both when there is only one", () => {
    const container = mount(`<button id="only">only</button>`);
    const edges = getTabbableEdges(container)!;

    expect(edges.first).toBe(edges.last);
  });

  it("returns null when there are no stops", () => {
    expect(getTabbableEdges(mount(`<p>text</p>`))).toBeNull();
  });
});

describe("focusFirst", () => {
  it("focuses the first tab stop", () => {
    const container = mount(`<button id="a">a</button><button id="b">b</button>`);

    expect(focusFirst(container)).toBe(true);
    expect(document.activeElement?.id).toBe("a");
  });

  it("falls back to the container when nothing inside is tabbable", () => {
    // Focus has to land somewhere inside, or a screen reader stays on the page
    // behind the dialog.
    const container = mount(`<p>nothing interactive</p>`);

    expect(focusFirst(container)).toBe(false);
    expect(document.activeElement).toBe(container);
    expect(container.getAttribute("tabindex")).toBe("-1");
  });

  it("does nothing for a null container", () => {
    expect(focusFirst(null)).toBe(false);
  });
});

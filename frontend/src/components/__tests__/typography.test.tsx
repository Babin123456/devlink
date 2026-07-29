/**
 * Unit tests for DevLink Typography System components.
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  TypoHero,
  TypoHeading,
  TypoSection,
  TypoCard,
  TypoBody,
  TypoCaption,
} from "@/components/shared/Typography";

describe("Typography components scale", () => {
  it("renders TypoHero as h1 by default", () => {
    render(<TypoHero>Hero Title</TypoHero>);
    const el = screen.getByRole("heading", { level: 1 });
    expect(el).toHaveTextContent("Hero Title");
  });

  it("renders TypoHeading as h2 by default", () => {
    render(<TypoHeading>Main Heading</TypoHeading>);
    const el = screen.getByRole("heading", { level: 2 });
    expect(el).toHaveTextContent("Main Heading");
  });

  it("renders TypoSection as h3 by default", () => {
    render(<TypoSection>Section Title</TypoSection>);
    const el = screen.getByRole("heading", { level: 3 });
    expect(el).toHaveTextContent("Section Title");
  });

  it("renders TypoCard as h4 by default", () => {
    render(<TypoCard>Card Title</TypoCard>);
    const el = screen.getByRole("heading", { level: 4 });
    expect(el).toHaveTextContent("Card Title");
  });

  it("renders TypoBody as paragraph", () => {
    render(<TypoBody>Body text content</TypoBody>);
    const el = screen.getByText("Body text content");
    expect(el.tagName).toBe("P");
  });

  it("renders TypoCaption as span", () => {
    render(<TypoCaption>Caption text</TypoCaption>);
    const el = screen.getByText("Caption text");
    expect(el.tagName).toBe("SPAN");
  });

  it("supports polymorphic 'as' prop", () => {
    render(<TypoHeading as="h1">Polymorphic H1</TypoHeading>);
    const el = screen.getByRole("heading", { level: 1 });
    expect(el).toHaveTextContent("Polymorphic H1");
  });

  it("applies custom classNames alongside default scale classes", () => {
    render(<TypoBody className="custom-test-class">Custom Body</TypoBody>);
    const el = screen.getByText("Custom Body");
    expect(el).toHaveClass("custom-test-class");
    expect(el).toHaveClass("font-normal");
  });
});

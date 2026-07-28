/**
 * Tests for the DevLink motion system components and configuration.
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { pageVariants, pageVariantsReduced, hoverElevation, DURATION } from "@/lib/motion";
import { AnimatedPage } from "@/components/shared/AnimatedPage";
import { MotionCard } from "@/components/shared/MotionCard";
import { AnimatedList, AnimatedListItem } from "@/components/shared/AnimatedList";

describe("Motion configuration", () => {
  it("pageVariants has required keys", () => {
    expect(pageVariants).toHaveProperty("initial");
    expect(pageVariants).toHaveProperty("animate");
    expect(pageVariants).toHaveProperty("exit");
  });

  it("pageVariantsReduced has zero duration in animate", () => {
    // Reduced motion animate should have 0 or no duration
    const animTransition = (pageVariantsReduced.animate as { transition?: { duration?: number } })
      ?.transition;
    expect(animTransition?.duration).toBe(0);
  });

  it("DURATION tokens are positive numbers", () => {
    expect(DURATION.fast).toBeGreaterThan(0);
    expect(DURATION.base).toBeGreaterThan(0);
    expect(DURATION.slow).toBeGreaterThan(0);
  });

  it("hoverElevation has whileHover and whileTap", () => {
    expect(hoverElevation).toHaveProperty("whileHover");
    expect(hoverElevation).toHaveProperty("whileTap");
  });
});

describe("AnimatedPage", () => {
  it("renders children without crashing", () => {
    render(
      <AnimatedPage>
        <div data-testid="child">Hello</div>
      </AnimatedPage>,
    );
    expect(screen.getByTestId("child")).toBeTruthy();
  });

  it("applies className to wrapper", () => {
    const { container } = render(
      <AnimatedPage className="test-class">
        <span />
      </AnimatedPage>,
    );
    expect(container.firstChild).toHaveClass("test-class");
  });
});

describe("MotionCard", () => {
  it("renders children without crashing", () => {
    render(
      <MotionCard>
        <p data-testid="card-child">Card content</p>
      </MotionCard>,
    );
    expect(screen.getByTestId("card-child")).toBeTruthy();
  });
});

describe("AnimatedList", () => {
  it("renders all list items", () => {
    render(
      <AnimatedList>
        <AnimatedListItem>
          <span data-testid="item-1">Item 1</span>
        </AnimatedListItem>
        <AnimatedListItem>
          <span data-testid="item-2">Item 2</span>
        </AnimatedListItem>
      </AnimatedList>,
    );
    expect(screen.getByTestId("item-1")).toBeTruthy();
    expect(screen.getByTestId("item-2")).toBeTruthy();
  });
});

import { describe, expect, it } from "vitest";

import {
  formatCompactNumber,
  formatDate,
  formatDateTime,
  formatNumber,
  formatPercent,
  formatRelativeTime,
} from "@/i18n/format";

const REFERENCE = new Date("2026-08-03T12:00:00Z");

describe("formatNumber", () => {
  it("uses the locale's grouping and decimal separators", () => {
    // The whole point of the exercise: en and es disagree about which
    // character means what.
    expect(formatNumber(1234.5, "en-US")).toBe("1,234.5");
    expect(formatNumber(1234.5, "de-DE")).toBe("1.234,5");
  });

  it("passes options through", () => {
    expect(formatNumber(0.5, "en-US", { minimumFractionDigits: 2 })).toBe("0.50");
  });

  it("returns an empty string for a non-finite value", () => {
    expect(formatNumber(Number.NaN, "en")).toBe("");
    expect(formatNumber(Number.POSITIVE_INFINITY, "en")).toBe("");
  });

  it("falls back to English for a malformed locale tag", () => {
    // A bad value in localStorage must not blank the page.
    expect(formatNumber(1234.5, "not a locale")).toBe("1,234.5");
  });
});

describe("formatPercent", () => {
  it("treats the input as a ratio", () => {
    expect(formatPercent(0.42, "en-US")).toBe("42%");
  });

  it("respects the fraction-digit cap", () => {
    expect(formatPercent(0.4267, "en-US", 1)).toBe("42.7%");
  });

  it("returns an empty string for a non-finite value", () => {
    expect(formatPercent(Number.NaN, "en")).toBe("");
  });
});

describe("formatCompactNumber", () => {
  it("shortens large values", () => {
    expect(formatCompactNumber(1200, "en-US")).toBe("1.2K");
    expect(formatCompactNumber(3_400_000, "en-US")).toBe("3.4M");
  });

  it("leaves small values alone", () => {
    expect(formatCompactNumber(42, "en-US")).toBe("42");
  });
});

describe("formatDate", () => {
  it("produces a locale-appropriate date", () => {
    const enResult = formatDate(REFERENCE, "en-US");
    const deResult = formatDate(REFERENCE, "de-DE");

    expect(enResult).toBeTruthy();
    expect(deResult).toBeTruthy();
    expect(enResult).not.toBe(deResult);
  });

  it("accepts an ISO string", () => {
    expect(formatDate("2026-08-03T12:00:00Z", "en-US")).toBeTruthy();
  });

  it("accepts a timestamp", () => {
    expect(formatDate(REFERENCE.getTime(), "en-US")).toBeTruthy();
  });

  it("returns an empty string for an unparseable value", () => {
    // Rendering "Invalid Date" at a user is never right.
    expect(formatDate("not a date", "en-US")).toBe("");
  });
});

describe("formatDateTime", () => {
  it("includes a time component", () => {
    const dateOnly = formatDate(REFERENCE, "en-US");
    const withTime = formatDateTime(REFERENCE, "en-US");

    expect(withTime.length).toBeGreaterThan(dateOnly.length);
  });
});

describe("formatRelativeTime", () => {
  it("describes the recent past", () => {
    const twoHoursAgo = new Date(REFERENCE.getTime() - 2 * 60 * 60 * 1000);

    expect(formatRelativeTime(twoHoursAgo, "en", REFERENCE)).toBe("2 hours ago");
  });

  it("describes the near future", () => {
    const inThreeDays = new Date(REFERENCE.getTime() + 3 * 24 * 60 * 60 * 1000);

    expect(formatRelativeTime(inThreeDays, "en", REFERENCE)).toBe("in 3 days");
  });

  it("uses natural wording where the locale has it", () => {
    // numeric: "auto" is what turns "1 day ago" into "yesterday".
    const yesterday = new Date(REFERENCE.getTime() - 24 * 60 * 60 * 1000);

    expect(formatRelativeTime(yesterday, "en", REFERENCE)).toBe("yesterday");
  });

  it("picks the largest sensible unit", () => {
    const lastYear = new Date(REFERENCE.getTime() - 400 * 24 * 60 * 60 * 1000);

    expect(formatRelativeTime(lastYear, "en", REFERENCE)).toContain("year");
  });

  it("handles sub-second differences", () => {
    expect(formatRelativeTime(REFERENCE, "en", REFERENCE)).toBe("now");
  });

  it("translates with the locale", () => {
    const twoHoursAgo = new Date(REFERENCE.getTime() - 2 * 60 * 60 * 1000);

    expect(formatRelativeTime(twoHoursAgo, "es", REFERENCE)).toBe("hace 2 horas");
  });

  it("returns an empty string for an unparseable value", () => {
    expect(formatRelativeTime("nonsense", "en", REFERENCE)).toBe("");
  });
});

/**
 * Locale-aware formatting helpers.
 *
 * The app currently formats dates with ad-hoc `date-fns` calls and numbers
 * with template strings, so a user whose browser is set to `de-DE` still sees
 * US conventions throughout. These wrap `Intl` so output follows the active
 * locale instead.
 *
 * Every helper is defensive about the locale tag: an unknown or malformed one
 * degrades to `en` rather than throwing, because a bad value in localStorage
 * should not blank out a page.
 */

const DEFAULT_FALLBACK_LOCALE = "en";

/** Formatter construction is expensive relative to how often we format. */
const dateFormatterCache = new Map<string, Intl.DateTimeFormat>();
const numberFormatterCache = new Map<string, Intl.NumberFormat>();
const relativeFormatterCache = new Map<string, Intl.RelativeTimeFormat>();

function cacheKey(locale: string, options: object): string {
  return `${locale}|${JSON.stringify(options)}`;
}

function getDateFormatter(
  locale: string,
  options: Intl.DateTimeFormatOptions,
): Intl.DateTimeFormat {
  const key = cacheKey(locale, options);
  let formatter = dateFormatterCache.get(key);

  if (!formatter) {
    try {
      formatter = new Intl.DateTimeFormat(locale, options);
    } catch {
      formatter = new Intl.DateTimeFormat(DEFAULT_FALLBACK_LOCALE, options);
    }
    dateFormatterCache.set(key, formatter);
  }

  return formatter;
}

function getNumberFormatter(locale: string, options: Intl.NumberFormatOptions): Intl.NumberFormat {
  const key = cacheKey(locale, options);
  let formatter = numberFormatterCache.get(key);

  if (!formatter) {
    try {
      formatter = new Intl.NumberFormat(locale, options);
    } catch {
      formatter = new Intl.NumberFormat(DEFAULT_FALLBACK_LOCALE, options);
    }
    numberFormatterCache.set(key, formatter);
  }

  return formatter;
}

function getRelativeFormatter(locale: string): Intl.RelativeTimeFormat {
  let formatter = relativeFormatterCache.get(locale);

  if (!formatter) {
    try {
      formatter = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
    } catch {
      formatter = new Intl.RelativeTimeFormat(DEFAULT_FALLBACK_LOCALE, {
        numeric: "auto",
      });
    }
    relativeFormatterCache.set(locale, formatter);
  }

  return formatter;
}

function toDate(value: Date | string | number): Date | null {
  const date = value instanceof Date ? value : new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

/**
 * Format a date, e.g. `3 Aug 2026` in `en-GB`, `3 ago 2026` in `es`.
 *
 * Returns an empty string for an unparseable value — rendering "Invalid Date"
 * at a user is never the right answer.
 */
export function formatDate(
  value: Date | string | number,
  locale: string,
  options: Intl.DateTimeFormatOptions = { dateStyle: "medium" },
): string {
  const date = toDate(value);
  if (!date) return "";

  return getDateFormatter(locale, options).format(date);
}

/** Format a date and time together. */
export function formatDateTime(
  value: Date | string | number,
  locale: string,
  options: Intl.DateTimeFormatOptions = {
    dateStyle: "medium",
    timeStyle: "short",
  },
): string {
  return formatDate(value, locale, options);
}

/** Thresholds for picking a relative-time unit, largest first. */
const RELATIVE_UNITS: Array<[Intl.RelativeTimeFormatUnit, number]> = [
  ["year", 60 * 60 * 24 * 365],
  ["month", 60 * 60 * 24 * 30],
  ["week", 60 * 60 * 24 * 7],
  ["day", 60 * 60 * 24],
  ["hour", 60 * 60],
  ["minute", 60],
  ["second", 1],
];

/**
 * Format a timestamp relative to now: "2 hours ago", "hace 2 horas".
 *
 * `numeric: "auto"` is what produces "yesterday" rather than "1 day ago" in
 * locales that have a word for it.
 */
export function formatRelativeTime(
  value: Date | string | number,
  locale: string,
  now: Date = new Date(),
): string {
  const date = toDate(value);
  if (!date) return "";

  const deltaSeconds = (date.getTime() - now.getTime()) / 1000;
  const absolute = Math.abs(deltaSeconds);

  for (const [unit, secondsInUnit] of RELATIVE_UNITS) {
    if (absolute >= secondsInUnit) {
      const amount = Math.round(deltaSeconds / secondsInUnit);
      return getRelativeFormatter(locale).format(amount, unit);
    }
  }

  // Under a second in either direction.
  return getRelativeFormatter(locale).format(0, "second");
}

/** Format a number: `1,234.5` in `en`, `1.234,5` in `es`. */
export function formatNumber(
  value: number,
  locale: string,
  options: Intl.NumberFormatOptions = {},
): string {
  if (!Number.isFinite(value)) return "";

  return getNumberFormatter(locale, options).format(value);
}

/**
 * Format a 0–1 ratio as a percentage.
 *
 * Takes a ratio rather than an already-multiplied number so callers cannot
 * disagree about whether `50` means 50% or 5000%.
 */
export function formatPercent(ratio: number, locale: string, maximumFractionDigits = 0): string {
  if (!Number.isFinite(ratio)) return "";

  return getNumberFormatter(locale, {
    style: "percent",
    maximumFractionDigits,
  }).format(ratio);
}

/**
 * Compact notation for large counts: `1.2K`, `3.4M`.
 *
 * Used for follower and view counts, where the exact figure is noise.
 */
export function formatCompactNumber(value: number, locale: string): string {
  if (!Number.isFinite(value)) return "";

  return getNumberFormatter(locale, {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

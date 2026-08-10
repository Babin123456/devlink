/**
 * English catalogue — the source of truth.
 *
 * Every key must exist here. Other locales are allowed to be incomplete; a
 * missing key falls back to the English string.
 *
 * Keys are flat and dot-separated, grouped by area. `as const` is what gives
 * `TranslationKey` exact autocomplete, so it must stay.
 */

export const en = {
  // ------------------------------------------------------------------
  // Shared vocabulary
  // ------------------------------------------------------------------
  "common.appName": "DevLink",
  "common.cancel": "Cancel",
  "common.save": "Save",
  "common.retry": "Retry",
  "common.goHome": "Go Home",
  "common.goBack": "Go Back",
  "common.goToLogin": "Go to Login",
  "common.loading": "Loading…",
  "common.search": "Search",
  "common.close": "Close",

  // ------------------------------------------------------------------
  // Error pages
  //
  // Status numerals stay in the string: they are the same in every locale,
  // and splitting them out would mean assembling the title in the component.
  // ------------------------------------------------------------------
  "errors.unauthorized.title": "401 • Unauthorized",
  "errors.unauthorized.description": "You need to sign in to access this page.",

  "errors.forbidden.title": "403 • Forbidden",
  "errors.forbidden.description": "You don't have permission to access this resource.",

  "errors.serverError.title": "500 • Server Error",
  "errors.serverError.description":
    "Something went wrong on our end. Please try again in a few moments.",

  "errors.network.title": "Network Error",
  "errors.network.description": "We couldn't reach the server. Please try again.",

  "errors.offline.title": "You're Offline",
  "errors.offline.description": "Please check your internet connection and try again.",

  // ------------------------------------------------------------------
  // Language switcher
  // ------------------------------------------------------------------
  "language.label": "Language",
  "language.change": "Change language",

  // ------------------------------------------------------------------
  // Pluralised counts
  // ------------------------------------------------------------------
  "projects.count": {
    one: "{count} project",
    other: "{count} projects",
  },
  "members.count": {
    one: "{count} member",
    other: "{count} members",
  },
  "notifications.unread": {
    zero: "No unread notifications",
    one: "{count} unread notification",
    other: "{count} unread notifications",
  },
} as const;

/**
 * Every valid translation key.
 *
 * Passing anything else to `t()` is a compile error, which is the main reason
 * to keep the catalogue flat and `as const`.
 */
export type TranslationKey = keyof typeof en;

export default en;

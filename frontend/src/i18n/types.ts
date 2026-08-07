/**
 * Core i18n types.
 *
 * Kept in their own module so the catalogues, the translator and the React
 * layer can all import them without pulling each other in.
 */

/**
 * Values substituted into a `{placeholder}` in a message.
 *
 * `undefined` is permitted so callers can pass an optional value straight
 * through; `interpolate` leaves the placeholder visible rather than printing
 * "undefined".
 */
export type InterpolationValues = Record<string, string | number | undefined>;

/**
 * A message with per-plural-category variants.
 *
 * Categories are the CLDR ones (`zero`, `one`, `two`, `few`, `many`, `other`)
 * as reported by `Intl.PluralRules`. Only `other` is required — English needs
 * `one` and `other`, Japanese needs only `other`, Polish needs four.
 */
export interface PluralForms {
  zero?: string;
  one?: string;
  two?: string;
  few?: string;
  many?: string;
  other: string;
}

/** A single catalogue entry: a plain message or a set of plural forms. */
export type Message = string | PluralForms;

/**
 * A catalogue: flat dot-separated keys to messages.
 *
 * Flat rather than nested on purpose. Nesting reads nicely in the file but
 * makes the key type a recursive conditional that is slow to check and awful
 * to read in an editor tooltip; `keyof typeof en` on a flat object gives exact
 * autocomplete for free.
 */
export type Catalogue = Record<string, Message>;

/** Options accepted by `t()`. */
export interface TranslateOptions extends InterpolationValues {
  /**
   * Selects a plural form and is also available as `{count}` for
   * interpolation, so `"{count} projects"` needs no second argument.
   */
  count?: number;
}

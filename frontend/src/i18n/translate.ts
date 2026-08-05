/**
 * Message resolution, interpolation and pluralisation.
 *
 * Everything here is pure — no React, no browser globals beyond `Intl` — so
 * the rules can be tested directly.
 */

import type {
  Catalogue,
  InterpolationValues,
  Message,
  PluralForms,
  TranslateOptions,
} from "./types";

/** Matches `{name}`, allowing incidental whitespace: `{ name }`. */
const PLACEHOLDER_PATTERN = /\{\s*([a-zA-Z0-9_]+)\s*\}/g;

/**
 * `Intl.PluralRules` instances are not cheap to build and we call this on
 * every render of every pluralised string.
 */
const pluralRulesCache = new Map<string, Intl.PluralRules>();

function getPluralRules(locale: string): Intl.PluralRules {
  let rules = pluralRulesCache.get(locale);

  if (!rules) {
    try {
      rules = new Intl.PluralRules(locale);
    } catch {
      // An unknown or malformed tag must not take the page down.
      rules = new Intl.PluralRules("en");
    }
    pluralRulesCache.set(locale, rules);
  }

  return rules;
}

/** Whether a message carries plural variants rather than being a plain string. */
export function isPluralForms(message: Message): message is PluralForms {
  return typeof message === "object" && message !== null && "other" in message;
}

/**
 * Substitute `{placeholder}` tokens.
 *
 * An unknown placeholder is left verbatim rather than replaced with
 * `undefined`. A visible `{userName}` in the UI is an obvious bug report; the
 * string "undefined" is a confusing one.
 */
export function interpolate(template: string, values: InterpolationValues = {}): string {
  return template.replace(PLACEHOLDER_PATTERN, (match, name: string) => {
    const value = values[name];
    return value === undefined || value === null ? match : String(value);
  });
}

/**
 * Pick the plural variant for `count` under `locale`.
 *
 * One deliberate deviation from CLDR: an explicit `zero` form is honoured at
 * `count === 0` in every locale. English has no `zero` plural category, so
 * strictly following `Intl.PluralRules` would mean a translator who wrote
 * `zero: "No unread notifications"` silently never saw it and got
 * "0 unread notifications" instead. Writing a `zero` form is an unambiguous
 * statement of intent, so it wins.
 *
 * Otherwise falls back to `other`, which every entry is required to define, so
 * a locale needing a category the translator did not supply still renders.
 */
export function selectPlural(forms: PluralForms, count: number, locale: string): string {
  if (count === 0 && forms.zero !== undefined) {
    return forms.zero;
  }

  const category = getPluralRules(locale).select(count);
  return forms[category] ?? forms.other;
}

/**
 * Turn a key into something readable for the last-resort fallback.
 *
 * `projects.emptyState.title` becomes "Title"; `common.tryAgain` becomes
 * "Try again". Not a translation, but far better than rendering a raw dotted
 * key at the user.
 */
export function humaniseKey(key: string): string {
  const segment = key.split(".").pop() ?? key;

  const spaced = segment
    .replace(/[_-]+/g, " ")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .trim()
    .toLowerCase();

  if (!spaced) return key;

  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

export interface TranslateContext {
  locale: string;
  catalogue: Catalogue;
  /** English, normally. Used when the active catalogue lacks the key. */
  fallbackCatalogue?: Catalogue;
  /** Called once per missing key. Wired to a dev-only console warning. */
  onMissingKey?: (key: string, locale: string) => void;
}

/**
 * Resolve a key to a finished string.
 *
 * Lookup order is active catalogue, then the fallback catalogue, then a
 * humanised form of the key itself. It never throws and never returns an empty
 * string, because a translation problem should degrade the copy, not blank out
 * the UI or crash a render.
 */
export function translate(
  key: string,
  options: TranslateOptions = {},
  context: TranslateContext,
): string {
  const { locale, catalogue, fallbackCatalogue, onMissingKey } = context;

  let message: Message | undefined = catalogue[key];

  if (message === undefined && fallbackCatalogue) {
    message = fallbackCatalogue[key];
  }

  if (message === undefined) {
    onMissingKey?.(key, locale);
    return humaniseKey(key);
  }

  const { count, ...rest } = options;
  const values: InterpolationValues = count === undefined ? rest : { ...rest, count };

  if (isPluralForms(message)) {
    if (count === undefined) {
      // Asking for a pluralised message without a count is a caller bug.
      // `other` is the sane guess; warning makes it findable.
      onMissingKey?.(`${key} (missing count)`, locale);
      return interpolate(message.other, values);
    }
    return interpolate(selectPlural(message, count, locale), values);
  }

  return interpolate(message, values);
}

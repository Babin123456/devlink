/**
 * Locale registry.
 *
 * Adding a language is: write the catalogue file, import it, add one entry
 * here. Nothing else in the app needs to change.
 */

import type { Catalogue } from "../types";

import { en } from "./en";
import { es } from "./es";

export const DEFAULT_LOCALE = "en";

export interface LocaleDefinition {
  code: string;
  /** Name in the language itself — "Español", not "Spanish". */
  nativeName: string;
  /** English name, for the accessible label. */
  englishName: string;
  catalogue: Catalogue;
}

export const LOCALES: Record<string, LocaleDefinition> = {
  en: {
    code: "en",
    nativeName: "English",
    englishName: "English",
    catalogue: en,
  },
  es: {
    code: "es",
    nativeName: "Español",
    englishName: "Spanish",
    catalogue: es,
  },
};

export const SUPPORTED_LOCALES = Object.keys(LOCALES);

/** The English catalogue, used as the fallback for every other locale. */
export const FALLBACK_CATALOGUE: Catalogue = en;

export function isSupportedLocale(locale: string): boolean {
  return locale in LOCALES;
}

/**
 * Map a browser language tag onto a locale we actually have.
 *
 * `navigator.language` gives things like `es-419` or `en-GB`. An exact match
 * wins; otherwise the primary subtag is tried, so `es-MX` resolves to `es`.
 * Returns `null` when nothing matches, leaving the caller to decide.
 */
export function resolveLocale(tag: string | undefined | null): string | null {
  if (!tag) return null;

  const normalised = tag.toLowerCase();
  if (isSupportedLocale(normalised)) return normalised;

  const primary = normalised.split("-")[0];
  if (isSupportedLocale(primary)) return primary;

  return null;
}

export function getCatalogue(locale: string): Catalogue {
  return LOCALES[locale]?.catalogue ?? FALLBACK_CATALOGUE;
}

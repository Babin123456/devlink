/**
 * DevLink internationalisation.
 *
 * Deliberately dependency-free rather than pulling in `react-i18next`. What
 * the app needs today is key lookup, `{placeholder}` interpolation, plural
 * selection and `Intl` formatting; that is a few hundred lines, against a
 * sizeable dependency with its own plugin system and initialisation dance.
 * If requirements grow past this — ICU message syntax, lazy-loaded namespaces,
 * translation-management tooling — swapping in a library behind the same
 * `useTranslation()` surface is a contained change.
 *
 * Locale is resolved as: stored preference → `navigator.language` → `en`.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  formatCompactNumber,
  formatDate,
  formatDateTime,
  formatNumber,
  formatPercent,
  formatRelativeTime,
} from "@/i18n/format";
import {
  DEFAULT_LOCALE,
  FALLBACK_CATALOGUE,
  LOCALES,
  getCatalogue,
  isSupportedLocale,
  resolveLocale,
  type LocaleDefinition,
} from "@/i18n/locales";
import type { TranslationKey } from "@/i18n/locales/en";
import { translate } from "@/i18n/translate";
import type { TranslateOptions } from "@/i18n/types";

const STORAGE_KEY = "devlink-locale";

export type TranslateFn = (key: TranslationKey, options?: TranslateOptions) => string;

interface I18nContextValue {
  locale: string;
  setLocale: (locale: string) => void;
  availableLocales: LocaleDefinition[];
  t: TranslateFn;
  formatDate: (value: Date | string | number, options?: Intl.DateTimeFormatOptions) => string;
  formatDateTime: (value: Date | string | number, options?: Intl.DateTimeFormatOptions) => string;
  formatRelativeTime: (value: Date | string | number, now?: Date) => string;
  formatNumber: (value: number, options?: Intl.NumberFormatOptions) => string;
  formatPercent: (ratio: number, maximumFractionDigits?: number) => string;
  formatCompactNumber: (value: number) => string;
}

const I18nContext = createContext<I18nContextValue | undefined>(undefined);

/** Keys already warned about, so a missing string does not spam the console. */
const warnedKeys = new Set<string>();

function warnOnce(key: string, locale: string) {
  if (!import.meta.env.DEV) return;

  const cacheKey = `${locale}:${key}`;
  if (warnedKeys.has(cacheKey)) return;

  warnedKeys.add(cacheKey);
  console.warn(`[i18n] Missing translation for "${key}" in locale "${locale}"`);
}

function getStoredLocale(): string | null {
  if (typeof window === "undefined") return null;

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved && isSupportedLocale(saved) ? saved : null;
  } catch (error) {
    // Safari in private mode throws on localStorage access.
    console.warn("Failed to read stored locale preference", error);
    return null;
  }
}

function detectInitialLocale(defaultLocale: string): string {
  if (typeof window === "undefined") return defaultLocale;

  const stored = getStoredLocale();
  if (stored) return stored;

  // `languages` is the user's ordered preference list; `language` is just the
  // first entry, so prefer the list when it is available.
  const candidates = navigator.languages?.length ? navigator.languages : [navigator.language];

  for (const candidate of candidates) {
    const resolved = resolveLocale(candidate);
    if (resolved) return resolved;
  }

  return defaultLocale;
}

interface I18nProviderProps {
  children: ReactNode;
  defaultLocale?: string;
}

export function I18nProvider({ children, defaultLocale = DEFAULT_LOCALE }: I18nProviderProps) {
  const [locale, setLocaleState] = useState<string>(() => detectInitialLocale(defaultLocale));

  // Keep <html lang> in step. Screen readers use it to pick a voice, and
  // browsers use it for hyphenation and translation prompts.
  useEffect(() => {
    if (typeof document === "undefined") return;
    document.documentElement.lang = locale;
  }, [locale]);

  const setLocale = useCallback((next: string) => {
    if (!isSupportedLocale(next)) {
      console.warn(`[i18n] Ignoring unsupported locale "${next}"`);
      return;
    }

    setLocaleState(next);

    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (error) {
      // Preference is lost on reload but the app keeps working.
      console.warn("Failed to persist locale preference", error);
    }
  }, []);

  const value = useMemo<I18nContextValue>(() => {
    const catalogue = getCatalogue(locale);

    const t: TranslateFn = (key, options) =>
      translate(key, options, {
        locale,
        catalogue,
        fallbackCatalogue: FALLBACK_CATALOGUE,
        onMissingKey: warnOnce,
      });

    return {
      locale,
      setLocale,
      availableLocales: Object.values(LOCALES),
      t,
      formatDate: (v, options) => formatDate(v, locale, options),
      formatDateTime: (v, options) => formatDateTime(v, locale, options),
      formatRelativeTime: (v, now) => formatRelativeTime(v, locale, now),
      formatNumber: (v, options) => formatNumber(v, locale, options),
      formatPercent: (ratio, digits) => formatPercent(ratio, locale, digits),
      formatCompactNumber: (v) => formatCompactNumber(v, locale),
    };
  }, [locale, setLocale]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

/**
 * Access the active locale, `t()`, and the formatting helpers.
 *
 * Throws outside a provider rather than silently falling back to English —
 * a component rendered outside the tree is a wiring bug, and quietly working
 * in English would hide it until a non-English user reported it.
 */
export function useTranslation(): I18nContextValue {
  const context = useContext(I18nContext);

  if (!context) {
    throw new Error("useTranslation must be used within an I18nProvider");
  }

  return context;
}

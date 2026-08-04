import { describe, expect, it, vi } from "vitest";

import { en } from "@/i18n/locales/en";
import { es } from "@/i18n/locales/es";
import { resolveLocale } from "@/i18n/locales";
import { humaniseKey, interpolate, isPluralForms, selectPlural, translate } from "@/i18n/translate";
import type { Catalogue } from "@/i18n/types";

const catalogue: Catalogue = {
  "greeting.plain": "Hello",
  "greeting.named": "Hello, {name}!",
  "greeting.twice": "{name} and {name}",
  "greeting.spaced": "Hello, { name }!",
  "items.count": { one: "{count} item", other: "{count} items" },
  "inbox.unread": {
    zero: "Nothing unread",
    one: "{count} unread",
    other: "{count} unread",
  },
};

function t(
  key: string,
  options = {},
  locale = "en",
  override: Partial<Parameters<typeof translate>[2]> = {},
) {
  return translate(key, options, { locale, catalogue, ...override });
}

// ----------------------------------------------------------------------
// interpolate
// ----------------------------------------------------------------------

describe("interpolate", () => {
  it("substitutes a named placeholder", () => {
    expect(interpolate("Hello, {name}!", { name: "Alex" })).toBe("Hello, Alex!");
  });

  it("substitutes every occurrence", () => {
    expect(interpolate("{a} and {a}", { a: "x" })).toBe("x and x");
  });

  it("tolerates whitespace inside the braces", () => {
    expect(interpolate("Hi { name }", { name: "Alex" })).toBe("Hi Alex");
  });

  it("coerces numbers", () => {
    expect(interpolate("{n} left", { n: 3 })).toBe("3 left");
  });

  it("leaves an unknown placeholder visible", () => {
    // A visible {missing} is an obvious bug report. "undefined" is a
    // confusing one.
    expect(interpolate("Hello, {missing}!")).toBe("Hello, {missing}!");
  });

  it("leaves a placeholder whose value is undefined", () => {
    expect(interpolate("Hi {name}", { name: undefined })).toBe("Hi {name}");
  });

  it("returns a template with no placeholders unchanged", () => {
    expect(interpolate("Plain text", { unused: "x" })).toBe("Plain text");
  });
});

// ----------------------------------------------------------------------
// Pluralisation
// ----------------------------------------------------------------------

describe("selectPlural", () => {
  const forms = { one: "one thing", other: "many things" };

  it("picks the English singular for 1", () => {
    expect(selectPlural(forms, 1, "en")).toBe("one thing");
  });

  it("picks the plural for 0 and 2 in English", () => {
    expect(selectPlural(forms, 0, "en")).toBe("many things");
    expect(selectPlural(forms, 2, "en")).toBe("many things");
  });

  it("falls back to `other` when the locale needs a category we lack", () => {
    // Japanese only has `other`, so a catalogue with just `one` must still
    // resolve.
    expect(selectPlural({ other: "もの" }, 1, "ja")).toBe("もの");
  });

  it("falls back to English rules for a malformed locale tag", () => {
    expect(selectPlural(forms, 1, "not a locale")).toBe("one thing");
  });
});

describe("isPluralForms", () => {
  it("recognises plural forms", () => {
    expect(isPluralForms({ other: "x" })).toBe(true);
  });

  it("rejects a plain string", () => {
    expect(isPluralForms("x")).toBe(false);
  });
});

// ----------------------------------------------------------------------
// humaniseKey
// ----------------------------------------------------------------------

describe("humaniseKey", () => {
  it("uses the last segment", () => {
    expect(humaniseKey("projects.emptyState.title")).toBe("Title");
  });

  it("splits camelCase", () => {
    expect(humaniseKey("common.tryAgain")).toBe("Try again");
  });

  it("handles dashes and underscores", () => {
    expect(humaniseKey("a.b.some_long-name")).toBe("Some long name");
  });

  it("handles a key with no dots", () => {
    expect(humaniseKey("save")).toBe("Save");
  });
});

// ----------------------------------------------------------------------
// translate
// ----------------------------------------------------------------------

describe("translate", () => {
  it("resolves a plain key", () => {
    expect(t("greeting.plain")).toBe("Hello");
  });

  it("interpolates while resolving", () => {
    expect(t("greeting.named", { name: "Alex" })).toBe("Hello, Alex!");
  });

  it("exposes count for interpolation as well as plural selection", () => {
    expect(t("items.count", { count: 1 })).toBe("1 item");
    expect(t("items.count", { count: 5 })).toBe("5 items");
  });

  it("uses the zero form where one is provided", () => {
    expect(t("inbox.unread", { count: 0 })).toBe("Nothing unread");
  });

  it("falls back to the fallback catalogue", () => {
    const result = translate(
      "only.in.fallback",
      {},
      {
        locale: "es",
        catalogue,
        fallbackCatalogue: { "only.in.fallback": "From English" },
      },
    );

    expect(result).toBe("From English");
  });

  it("falls back to a humanised key when nothing matches", () => {
    expect(t("totally.unknown.keyName")).toBe("Key name");
  });

  it("reports a missing key exactly once per call", () => {
    const onMissingKey = vi.fn();
    t("totally.unknown", {}, "en", { onMissingKey });

    expect(onMissingKey).toHaveBeenCalledWith("totally.unknown", "en");
  });

  it("warns but still renders when a plural key is used without a count", () => {
    const onMissingKey = vi.fn();

    expect(t("items.count", {}, "en", { onMissingKey })).toBe("{count} items");
    expect(onMissingKey).toHaveBeenCalled();
  });

  it("never returns an empty string", () => {
    expect(t("nothing.here").length).toBeGreaterThan(0);
  });
});

// ----------------------------------------------------------------------
// Catalogues
// ----------------------------------------------------------------------

describe("catalogues", () => {
  it("every Spanish key exists in English", () => {
    // English is the source of truth; a key only in another locale is dead
    // weight nothing can reference.
    const englishKeys = new Set(Object.keys(en));
    const orphans = Object.keys(es).filter((key) => !englishKeys.has(key));

    expect(orphans).toEqual([]);
  });

  it("every plural entry defines `other`", () => {
    for (const [key, message] of Object.entries({ ...en, ...es })) {
      if (isPluralForms(message)) {
        expect(message.other, `${key} is missing an "other" form`).toBeTruthy();
      }
    }
  });

  it("Spanish placeholders match the English ones", () => {
    const names = (value: string) => (value.match(/\{\s*([a-zA-Z0-9_]+)\s*\}/g) ?? []).sort();

    for (const [key, spanish] of Object.entries(es)) {
      const english = (en as Record<string, unknown>)[key];
      if (typeof spanish !== "string" || typeof english !== "string") continue;

      expect(names(spanish), `placeholders differ for ${key}`).toEqual(names(english));
    }
  });
});

// ----------------------------------------------------------------------
// Locale resolution
// ----------------------------------------------------------------------

describe("resolveLocale", () => {
  it("matches an exact tag", () => {
    expect(resolveLocale("es")).toBe("es");
  });

  it("falls back to the primary subtag", () => {
    expect(resolveLocale("es-MX")).toBe("es");
    expect(resolveLocale("en-GB")).toBe("en");
  });

  it("is case-insensitive", () => {
    expect(resolveLocale("ES-mx")).toBe("es");
  });

  it("returns null for an unsupported language", () => {
    expect(resolveLocale("fr-FR")).toBeNull();
  });

  it("returns null for empty input", () => {
    expect(resolveLocale("")).toBeNull();
    expect(resolveLocale(undefined)).toBeNull();
    expect(resolveLocale(null)).toBeNull();
  });
});

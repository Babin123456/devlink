import { Languages } from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useTranslation } from "@/context/I18nContext";

interface LanguageSwitcherProps {
  /** Hide the leading icon where space is tight. */
  showIcon?: boolean;
  className?: string;
}

/**
 * Locale picker.
 *
 * Options are labelled in their own language ("Español", not "Spanish") —
 * somebody looking for their language will not necessarily recognise the
 * English name for it. The English name goes in the `aria-label` so the
 * accessible name is still useful.
 */
export function LanguageSwitcher({ showIcon = true, className }: LanguageSwitcherProps) {
  const { locale, setLocale, availableLocales, t } = useTranslation();

  return (
    <div className={className}>
      <Select value={locale} onValueChange={setLocale}>
        <SelectTrigger aria-label={t("language.change")} className="w-auto gap-2">
          {showIcon ? <Languages className="h-4 w-4 shrink-0" aria-hidden="true" /> : null}
          <SelectValue placeholder={t("language.label")} />
        </SelectTrigger>

        <SelectContent>
          {availableLocales.map((definition) => (
            <SelectItem
              key={definition.code}
              value={definition.code}
              aria-label={definition.englishName}
            >
              {definition.nativeName}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

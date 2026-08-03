import { ShieldAlert } from "lucide-react";

import { useTranslation } from "@/context/I18nContext";

import { ErrorLayout } from "./ErrorLayout";

export function ForbiddenPage() {
  const { t } = useTranslation();

  return (
    <ErrorLayout
      icon={<ShieldAlert className="h-16 w-16 text-destructive" />}
      title={t("errors.forbidden.title")}
      description={t("errors.forbidden.description")}
    />
  );
}

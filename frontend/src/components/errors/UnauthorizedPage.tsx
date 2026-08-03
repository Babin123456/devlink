import { Lock } from "lucide-react";

import { useTranslation } from "@/context/I18nContext";

import { ErrorLayout } from "./ErrorLayout";

export function UnauthorizedPage() {
  const { t } = useTranslation();

  return (
    <ErrorLayout
      icon={<Lock className="h-16 w-16 text-warning" />}
      title={t("errors.unauthorized.title")}
      description={t("errors.unauthorized.description")}
      primaryLabel={t("common.goToLogin")}
      primaryTo="/auth"
    />
  );
}

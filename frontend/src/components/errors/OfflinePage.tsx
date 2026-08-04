import { WifiOff } from "lucide-react";

import { useTranslation } from "@/context/I18nContext";

import { ErrorLayout } from "./ErrorLayout";

export function OfflinePage() {
  const { t } = useTranslation();

  return (
    <ErrorLayout
      icon={<WifiOff className="h-16 w-16 text-muted-foreground" />}
      title={t("errors.offline.title")}
      description={t("errors.offline.description")}
      primaryLabel={t("common.retry")}
      primaryTo="/"
    />
  );
}

import { GlobeX } from "lucide-react";

import { useTranslation } from "@/context/I18nContext";

import { ErrorLayout } from "./ErrorLayout";

export function NetworkErrorPage() {
  const { t } = useTranslation();

  return (
    <ErrorLayout
      icon={<GlobeX className="h-16 w-16 text-warning" />}
      title={t("errors.network.title")}
      description={t("errors.network.description")}
      primaryLabel={t("common.retry")}
      primaryTo="/"
    />
  );
}

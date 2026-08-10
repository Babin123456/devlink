import { TriangleAlert } from "lucide-react";

import { useTranslation } from "@/context/I18nContext";

import { ErrorLayout } from "./ErrorLayout";

export function ServerErrorPage() {
  const { t } = useTranslation();

  return (
    <ErrorLayout
      icon={<TriangleAlert className="h-16 w-16 text-warning" />}
      title={t("errors.serverError.title")}
      description={t("errors.serverError.description")}
    />
  );
}

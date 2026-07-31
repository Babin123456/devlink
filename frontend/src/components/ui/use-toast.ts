import { toast as showToast } from "sonner";

type ToastVariant = "default" | "destructive";

interface ToastOptions {
  title?: string;
  description?: string;
  variant?: ToastVariant;
}

export function useToast() {
  const toast = (options: ToastOptions) => {
    const title = options.title ?? "";
    const description = options.description;
    if (options.variant === "destructive") {
      showToast.error(title, { description });
    } else {
      showToast(title, { description });
    }
  };
  return { toast };
}

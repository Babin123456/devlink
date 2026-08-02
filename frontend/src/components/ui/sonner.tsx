import { Toaster as Sonner } from "sonner";
import { useTheme } from "@/context/ThemeContext";

type ToasterProps = React.ComponentProps<typeof Sonner>;

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme } = useTheme();

  return (
    <Sonner
      theme={theme as "light" | "dark" | "system"}
      className="toaster group"
      richColors
      closeButton
      aria-label="Notification toasts"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg group-[.toaster]:rounded-lg group-[.toaster]:p-4 group-[.toaster]:text-sm group-[.toaster]:font-medium transition-all duration-200",
          description: "group-[.toast]:text-muted-foreground group-[.toast]:text-xs group-[.toast]:mt-1",
          actionButton: "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground group-[.toast]:font-semibold group-[.toast]:text-xs group-[.toast]:px-2.5 group-[.toast]:py-1 group-[.toast]:rounded-md",
          cancelButton: "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground group-[.toast]:text-xs group-[.toast]:px-2.5 group-[.toast]:py-1 group-[.toast]:rounded-md",
          closeButton: "group-[.toast]:bg-background group-[.toast]:border-border group-[.toast]:text-muted-foreground hover:group-[.toast]:text-foreground focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none",
          success: "group-[.toaster]:border-emerald-500/30 group-[.toaster]:bg-emerald-500/10 group-[.toaster]:text-emerald-900 dark:group-[.toaster]:text-emerald-100",
          error: "group-[.toaster]:border-rose-500/30 group-[.toaster]:bg-rose-500/10 group-[.toaster]:text-rose-900 dark:group-[.toaster]:text-rose-100",
          warning: "group-[.toaster]:border-amber-500/30 group-[.toaster]:bg-amber-500/10 group-[.toaster]:text-amber-900 dark:group-[.toaster]:text-amber-100",
          info: "group-[.toaster]:border-sky-500/30 group-[.toaster]:bg-sky-500/10 group-[.toaster]:text-sky-900 dark:group-[.toaster]:text-sky-100",
        },
      }}
      {...props}
    />
  );
};

export { Toaster };

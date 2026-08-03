import React, { useState, useEffect } from "react";
import { Mail, X, Send, CheckCircle2, AlertCircle } from "lucide-react";
import { toast } from "@/components/ui/use-toast";
import { cn } from "@/lib/utils";

export interface EmailVerificationBannerProps {
  isVerified?: boolean;
  userEmail?: string;
  onResendVerification?: () => Promise<void>;
  className?: string;
}

const STORAGE_KEY = "devlink_email_banner_dismissed_session";

export function EmailVerificationBanner({
  isVerified = false,
  userEmail,
  onResendVerification,
  className,
}: EmailVerificationBannerProps) {
  const [dismissed, setDismissed] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Only show if user is NOT verified and session has not dismissed the banner
    const isDismissedInSession = sessionStorage.getItem(STORAGE_KEY) === "true";
    if (!isVerified && !isDismissedInSession) {
      setDismissed(false);
    }
  }, [isVerified]);

  if (isVerified || dismissed) {
    return null;
  }

  const handleDismiss = () => {
    setDismissed(true);
    sessionStorage.setItem(STORAGE_KEY, "true");
  };

  const handleResend = async () => {
    setLoading(true);
    try {
      if (onResendVerification) {
        await onResendVerification();
      } else {
        // Default API request if no custom handler passed
        const res = await fetch("/api/auth/resend-verification", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: userEmail }),
        });
        if (!res.ok) throw new Error("Failed to send verification email");
      }

      toast.success("Verification Email Sent", {
        description: `We've sent a new confirmation link to ${userEmail || "your email"}.`,
      });
    } catch (err) {
      toast.error("Failed to Resend Email", {
        description: "Please try again later or contact support.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside
      role="region"
      aria-label="Email verification reminder"
      className={cn(
        "relative w-full bg-gradient-to-r from-amber-500/15 via-amber-500/10 to-transparent border-b border-amber-500/30 px-4 py-3 text-amber-950 dark:text-amber-100 backdrop-blur-sm transition-all",
        className,
      )}
    >
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 text-xs sm:text-sm">
        <div className="flex items-center gap-2.5">
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-amber-500/20 text-amber-600 dark:text-amber-400 shrink-0">
            <Mail className="h-4 w-4" aria-hidden="true" />
          </span>
          <p className="font-medium leading-tight">
            <strong className="font-semibold">Verify your email address:</strong> Please check your
            inbox
            {userEmail ? ` (${userEmail})` : ""} to activate all account capabilities.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={handleResend}
            disabled={loading}
            className="inline-flex items-center gap-1.5 rounded-md bg-amber-600 px-3 py-1.5 text-xs font-semibold text-white transition-all hover:bg-amber-700 active:scale-95 disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500 focus-visible:ring-offset-2"
          >
            <Send className="h-3.5 w-3.5" />
            {loading ? "Sending..." : "Resend Verification Email"}
          </button>

          <button
            type="button"
            onClick={handleDismiss}
            aria-label="Dismiss email verification reminder"
            className="rounded-md p-1.5 text-amber-700 dark:text-amber-300 hover:bg-amber-500/20 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}

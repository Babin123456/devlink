import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { EmailVerificationBanner } from "../EmailVerificationBanner";

describe("EmailVerificationBanner Component (#592)", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it("renders when user is unverified and session is not dismissed", () => {
    render(<EmailVerificationBanner isVerified={false} userEmail="test@example.com" />);
    expect(screen.getByText(/Verify your email address/i)).toBeInTheDocument();
    expect(screen.getByText(/test@example.com/i)).toBeInTheDocument();
  });

  it("does not render when user is verified", () => {
    render(<EmailVerificationBanner isVerified={true} userEmail="test@example.com" />);
    expect(screen.queryByText(/Verify your email address/i)).not.toBeInTheDocument();
  });

  it("allows dismissing banner until session ends", () => {
    render(<EmailVerificationBanner isVerified={false} userEmail="test@example.com" />);
    const dismissBtn = screen.getByLabelText(/Dismiss email verification reminder/i);
    fireEvent.click(dismissBtn);

    expect(screen.queryByText(/Verify your email address/i)).not.toBeInTheDocument();
    expect(sessionStorage.getItem("devlink_email_banner_dismissed_session")).toBe("true");
  });

  it("triggers resend verification callback on click", async () => {
    const handleResend = vi.fn().mockResolvedValue(undefined);
    render(
      <EmailVerificationBanner
        isVerified={false}
        userEmail="test@example.com"
        onResendVerification={handleResend}
      />,
    );

    const resendBtn = screen.getByRole("button", { name: /Resend Verification Email/i });
    fireEvent.click(resendBtn);

    await waitFor(() => {
      expect(handleResend).toHaveBeenCalledTimes(1);
    });
  });
});

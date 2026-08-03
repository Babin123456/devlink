import React from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { APP_LOGO } from "@/lib/logo";
import { motion } from "framer-motion";
import { Sparkles, Users2, MessageSquare, Trophy, Github, ArrowRight, Check } from "lucide-react";
import { Sun, Moon, X, Menu } from "lucide-react";
import { AnimatePresence } from "framer-motion";
import { useTheme } from "@/hooks/useTheme";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "DevLink — Find your next collaborator" },
      {
        name: "description",
        content:
          "DevLink is a developer collaboration platform. Match with builders using AI, run projects together, chat in real time, and win hackathons.",
      },
      { property: "og:title", content: "DevLink — Find your next collaborator" },
      {
        property: "og:description",
        content: "AI-powered matching, projects, messaging and hackathons in one place.",
      },
    ],
  }),
  component: Landing,
});

function Landing() {
  const { isDark, toggleTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [billingCycle, setBillingCycle] = React.useState<"monthly" | "yearly">("yearly");

  React.useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileMenuOpen]);
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-20 border-b border-border bg-surface/80 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center gap-4 px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2">
            <img src={APP_LOGO} alt="" className="h-9 w-9 rounded-md" />
            <span className="text-[20px] font-bold tracking-tight text-foreground">DevLink</span>
          </Link>
          <nav className="ml-6 hidden items-center gap-5 text-[13px] font-medium text-muted-foreground md:flex">
            <a href="#features" className="hover:text-foreground">
              Features
            </a>
            <Link to="/builders" className="hover:text-foreground">
              Builders
            </Link>
            <a href="#pricing" className="hover:text-foreground">
              Pricing
            </a>
          </nav>
          <div className="ml-auto flex items-center gap-2">
            <button
              type="button"
              onClick={toggleTheme}
              aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
              title={isDark ? "Switch to light mode" : "Switch to dark mode"}
              className="grid h-9 w-9 place-items-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
            >
              {isDark ? <Sun size={16} /> : <Moon size={16} />}
            </button>
            <button
              type="button"
              className="md:hidden rounded-md p-2 hover:bg-muted"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>

            <div className="hidden md:flex items-center gap-2">
              <Link
                to="/auth"
                className="rounded-md px-3 py-1.5 text-[13px] font-medium text-foreground hover:bg-muted"
              >
                Sign in
              </Link>

              <Link
                to="/auth"
                className="rounded-md bg-primary px-3 py-1.5 text-[13px] font-semibold text-primary-foreground hover:opacity-90"
              >
                Get started
              </Link>
            </div>
          </div>
        </div>
      </header>
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.2 }}
            className="md:hidden border-b border-border bg-surface"
          >
            <div className="flex flex-col px-4 py-4 space-y-3">
              <a
                href="#features"
                className="text-sm text-foreground"
                onClick={() => setMobileMenuOpen(false)}
              >
                Features
              </a>

              <Link
                to="/builders"
                className="text-sm text-foreground"
                onClick={() => setMobileMenuOpen(false)}
              >
                Builders
              </Link>

              <a
                href="#pricing"
                className="text-sm text-foreground"
                onClick={() => setMobileMenuOpen(false)}
              >
                Pricing
              </a>

              <Link
                to="/auth"
                onClick={() => setMobileMenuOpen(false)}
                className="rounded-md border border-border px-3 py-2 text-center"
              >
                Sign In
              </Link>

              <Link
                to="/auth"
                onClick={() => setMobileMenuOpen(false)}
                className="rounded-md bg-primary px-3 py-2 text-center text-primary-foreground"
              >
                Get Started
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <section className="border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-24 text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-surface px-3 py-1 text-[12px] font-medium text-muted-foreground">
              <Sparkles size={12} className="text-primary" /> AI-powered team matching · in beta
            </span>
            <h1 className="mx-auto mt-6 max-w-3xl text-[36px] font-bold leading-tight tracking-tight text-foreground sm:text-[52px]">
              Where builders connect, <span className="text-primary">collaborate</span> and ship.
            </h1>
            <p className="mx-auto mt-4 max-w-xl text-[15px] text-muted-foreground">
              Match with teammates by skills and vibe, run projects with real-time messaging, and
              enter hackathons together — all in one clean workspace.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link
                to="/auth"
                className="inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-[14px] font-semibold text-primary-foreground hover:opacity-90"
              >
                Start free <ArrowRight size={14} />
              </Link>
              <Link
                to="/auth"
                className="inline-flex items-center gap-1.5 rounded-md border border-border bg-surface px-4 py-2 text-[14px] font-medium text-foreground hover:bg-muted"
              >
                <Github size={14} /> Continue with GitHub
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section id="features" className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-4 px-4 py-16 sm:grid-cols-2 sm:px-6 lg:grid-cols-4">
          {[
            {
              icon: Sparkles,
              title: "AI matches",
              desc: "Rank teammates by skill, availability and past work.",
            },
            {
              icon: Users2,
              title: "Builder profiles",
              desc: "One profile, everywhere. Skills, stack, contributions.",
            },
            {
              icon: MessageSquare,
              title: "Real-time chat",
              desc: "Threaded conversations with your team, in-app.",
            },
            {
              icon: Trophy,
              title: "Hackathons",
              desc: "Discover jams, form teams, ship in a weekend.",
            },
          ].map((f) => (
            <div key={f.title} className="rounded-md border border-border bg-card p-5">
              <span className="grid h-9 w-9 place-items-center rounded-md bg-primary-soft text-primary">
                <f.icon size={16} />
              </span>
              <p className="mt-3 text-[15px] font-semibold text-foreground">{f.title}</p>
              <p className="mt-1 text-[13px] text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="pricing" className="border-b border-border py-24">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Simple, transparent pricing
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Start for free, upgrade when you need more power.
            </p>
          </div>

          <div className="mt-10 flex justify-center">
            <div className="relative flex rounded-full bg-muted p-1">
              <button
                type="button"
                onClick={() => setBillingCycle("monthly")}
                className={`relative w-32 rounded-full py-2 text-sm font-semibold transition-colors duration-200 ease-in-out ${
                  billingCycle === "monthly"
                    ? "text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {billingCycle === "monthly" && (
                  <motion.div
                    layoutId="billingCycle"
                    className="absolute inset-0 rounded-full bg-surface shadow-sm"
                    initial={false}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
                <span className="relative z-10">Monthly</span>
              </button>
              <button
                type="button"
                onClick={() => setBillingCycle("yearly")}
                className={`relative w-32 rounded-full py-2 text-sm font-semibold transition-colors duration-200 ease-in-out ${
                  billingCycle === "yearly"
                    ? "text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {billingCycle === "yearly" && (
                  <motion.div
                    layoutId="billingCycle"
                    className="absolute inset-0 rounded-full bg-surface shadow-sm"
                    initial={false}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
                <span className="relative z-10">Yearly</span>
                <span className="absolute -top-3 -right-2 rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary">
                  Save 20%
                </span>
              </button>
            </div>
          </div>

          <div className="mx-auto mt-12 grid max-w-4xl gap-8 lg:grid-cols-2">
            {[
              {
                name: "Hobby",
                desc: "Perfect for students and solo developers.",
                price: "$0",
                period: "forever",
                cta: "Get Started Free",
                perks: [
                  "Up to 3 active projects",
                  "Basic AI matching",
                  "Community feed access",
                  "Standard support",
                ],
              },
              {
                name: "Pro",
                desc: "For professionals who need more power.",
                price: billingCycle === "yearly" ? "$12" : "$15",
                period: "per user/month",
                cta: "Upgrade to Pro",
                featured: true,
                recommended: true,
                perks: [
                  "Unlimited projects",
                  "Priority AI matching & insights",
                  "Team analytics dashboard",
                  "Priority 24/7 support",
                  "Custom domain support",
                ],
              },
            ].map((p) => (
              <div
                key={p.name}
                className={`relative flex flex-col rounded-2xl border p-8 shadow-sm transition-all duration-200 hover:shadow-md ${
                  p.featured
                    ? "border-primary bg-primary-soft/10 ring-1 ring-primary/20"
                    : "border-border bg-card"
                }`}
              >
                {p.recommended && (
                  <div className="absolute -top-4 left-0 right-0 mx-auto w-32 rounded-full bg-primary px-3 py-1 text-center text-xs font-semibold text-primary-foreground shadow-sm">
                    Recommended
                  </div>
                )}
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-foreground">{p.name}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{p.desc}</p>
                </div>

                <div className="mb-6 flex items-baseline gap-2">
                  <span className="text-4xl font-bold tracking-tight text-foreground">
                    {p.price}
                  </span>
                  <span className="text-sm font-medium text-muted-foreground">{p.period}</span>
                </div>

                <Link
                  to="/auth"
                  className={`mb-8 inline-flex w-full items-center justify-center rounded-lg px-4 py-3 text-sm font-semibold transition-all ${
                    p.featured
                      ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm"
                      : "border border-border bg-surface text-foreground hover:bg-muted"
                  }`}
                >
                  {p.cta}
                </Link>

                <div className="flex-1">
                  <p className="mb-4 text-sm font-medium text-foreground">What's included:</p>
                  <ul className="space-y-3 text-sm text-muted-foreground">
                    {p.perks.map((perk) => (
                      <li key={perk} className="flex items-start gap-3">
                        <Check className="h-5 w-5 shrink-0 text-success" />
                        <span>{perk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-border bg-surface py-3">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-2 sm:flex-row sm:text-left">
          <div className="flex items-center gap-2">
            <img src={APP_LOGO} alt="Devlink Logo" className="h-12 w-12 rounded" />
            <span className="text-[20px] font-bold text-foreground ">DevLink</span>
            <span className="text-[11px] text-muted-foreground opacity-70">
              © {new Date().getFullYear()}
            </span>
          </div>
          <div className="flex items-center gap-5 text-[16px] text-muted-foreground">
            {[
              { label: "GitHub", href: "https://github.com/nensii21/devlink" },
              { label: "Privacy Policy", href: "#" },
              { label: "Terms", href: "#" },
              { label: "Contact", href: "#" },
            ].map((item) => (
              <a
                key={item.label}
                href={item.href}
                target={item.href.startsWith("http") ? "_blank" : undefined}
                rel={item.href.startsWith("http") ? "noopener noreferrer" : undefined}
                className="hover:text-primary hover:underline"
              >
                {item.label}
              </a>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}

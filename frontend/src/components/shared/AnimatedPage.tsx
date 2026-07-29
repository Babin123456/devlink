/**
 * AnimatedPage — wraps any page/route component with a page-level fade+slide
 * transition, respecting the user's `prefers-reduced-motion` setting.
 *
 * Usage:
 *   export default function DashboardPage() {
 *     return (
 *       <AnimatedPage>
 *         <Dashboard />
 *       </AnimatedPage>
 *     );
 *   }
 */

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";
import { pageVariants, pageVariantsReduced } from "@/lib/motion";

interface AnimatedPageProps {
  children: ReactNode;
  className?: string;
}

export function AnimatedPage({ children, className }: AnimatedPageProps) {
  const shouldReduce = useReducedMotion();
  const variants = shouldReduce ? pageVariantsReduced : pageVariants;

  return (
    <motion.div
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
      className={className}
      style={{ width: "100%" }}
    >
      {children}
    </motion.div>
  );
}

/**
 * MotionCard — a card surface that elevates on hover.
 *
 * Wraps any content and applies the standardized hover-elevation micro-animation
 * from the DevLink motion system. Respects `prefers-reduced-motion`.
 *
 * Usage:
 *   <MotionCard className="rounded-xl border bg-card p-4">
 *     <ProjectSummary project={project} />
 *   </MotionCard>
 */

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";
import { hoverElevation, hoverElevationReduced } from "@/lib/motion";

interface MotionCardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export function MotionCard({ children, className, onClick }: MotionCardProps) {
  const shouldReduce = useReducedMotion();
  const elevation = shouldReduce ? hoverElevationReduced : hoverElevation;

  return (
    <motion.div
      className={cn("cursor-default", className)}
      whileHover={elevation.whileHover}
      whileTap={elevation.whileTap}
      onClick={onClick}
      style={{ willChange: "transform" }}
    >
      {children}
    </motion.div>
  );
}

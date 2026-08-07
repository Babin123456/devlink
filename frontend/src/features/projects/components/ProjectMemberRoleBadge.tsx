import React from "react";
import { Crown, Shield, Code, CheckCircle, Eye, User } from "lucide-react";

export type ProjectRole =
  "owner" | "co_owner" | "admin" | "maintainer" | "contributor" | "reviewer" | "viewer" | "member";

interface ProjectMemberRoleBadgeProps {
  role: ProjectRole | string;
}

export const ProjectMemberRoleBadge: React.FC<ProjectMemberRoleBadgeProps> = ({ role }) => {
  const normalizedRole = (role || "").toLowerCase();

  switch (normalizedRole) {
    case "owner":
    case "co_owner":
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950 text-amber-300 border border-amber-800/60 shadow-sm">
          <Crown size={12} className="text-amber-400" />
          Project Owner
        </span>
      );
    case "maintainer":
    case "admin":
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-950 text-indigo-300 border border-indigo-800/60 shadow-sm">
          <Shield size={12} className="text-indigo-400" />
          Maintainer
        </span>
      );
    case "contributor":
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-950 text-blue-300 border border-blue-800/60 shadow-sm">
          <Code size={12} className="text-blue-400" />
          Contributor
        </span>
      );
    case "reviewer":
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800/60 shadow-sm">
          <CheckCircle size={12} className="text-emerald-400" />
          Reviewer
        </span>
      );
    case "viewer":
    case "member":
    default:
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-900 text-gray-400 border border-gray-800 shadow-sm">
          <Eye size={12} className="text-gray-400" />
          Viewer
        </span>
      );
  }
};

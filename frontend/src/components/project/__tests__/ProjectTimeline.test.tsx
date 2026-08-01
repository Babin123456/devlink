import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ProjectTimeline, TimelineEvent } from "../ProjectTimeline";

describe("ProjectTimeline Component (#591)", () => {
  it("renders default timeline events accurately", () => {
    render(<ProjectTimeline />);
    expect(screen.getByText("Project Created")).toBeInTheDocument();
    expect(screen.getByText("Recruitment Started")).toBeInTheDocument();
    expect(screen.getByText("Members Joined")).toBeInTheDocument();
    expect(screen.getByText("Milestones Completed")).toBeInTheDocument();
    expect(screen.getByText("Archived")).toBeInTheDocument();
  });

  it("supports dynamic event data", () => {
    const customEvents: TimelineEvent[] = [
      {
        id: "custom-1",
        type: "project_created",
        title: "Custom Launch Event",
        description: "Custom project launched successfully",
        timestamp: "2026-05-10T12:00:00Z",
        status: "completed",
      },
    ];

    render(<ProjectTimeline events={customEvents} />);
    expect(screen.getByText("Custom Launch Event")).toBeInTheDocument();
    expect(screen.getByText("Custom project launched successfully")).toBeInTheDocument();
  });
});

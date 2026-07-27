from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import cast, func, select, String
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_view import ProjectView
from app.schemas.project_analytics import DailyViewMetric, ProjectAnalyticsResponse


class ProjectAnalyticsService:
    """
    Business logic for tracking and calculating project page view analytics.
    """

    @staticmethod
    def record_view(
        db: Session,
        project_id: uuid.UUID,
        viewer_id: Optional[uuid.UUID] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[ProjectView]:
        project = db.get(Project, project_id)
        if not project:
            return None

        # Truncate user_agent if needed to fit schema max length
        if user_agent and len(user_agent) > 512:
            user_agent = user_agent[:512]

        view_event = ProjectView(
            project_id=project_id,
            viewer_id=viewer_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(view_event)

        # Update cached total views count on project table
        project.views = (project.views or 0) + 1
        db.commit()
        db.refresh(view_event)
        return view_event

    @staticmethod
    def get_analytics(
        db: Session,
        project_id: uuid.UUID,
        days: int = 30,
    ) -> ProjectAnalyticsResponse:
        project = db.get(Project, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=days)

        # Total views query
        total_views_stmt = select(func.count(ProjectView.id)).where(
            ProjectView.project_id == project_id
        )
        recorded_total = db.scalar(total_views_stmt) or 0
        total_views = max(recorded_total, project.views or 0)

        # Unique viewers query (distinct viewer_id or ip_address)
        unique_stmt = select(
            func.count(
                func.distinct(
                    func.coalesce(
                        cast(ProjectView.viewer_id, String),
                        ProjectView.ip_address,
                    )
                )
            )
        ).where(ProjectView.project_id == project_id)
        unique_viewers = db.scalar(unique_stmt) or 0

        # Daily views breakdown query for the last N days
        views_events = db.scalars(
            select(ProjectView).where(
                ProjectView.project_id == project_id,
                ProjectView.created_at >= start_date,
            )
        ).all()

        daily_data: Dict[str, Dict[str, set]] = {}

        for event in views_events:
            date_str = event.created_at.strftime("%Y-%m-%d")
            if date_str not in daily_data:
                daily_data[date_str] = {"views": 0, "unique_keys": set()}

            daily_data[date_str]["views"] += 1
            key = (
                str(event.viewer_id)
                if event.viewer_id
                else (event.ip_address or str(event.id))
            )
            daily_data[date_str]["unique_keys"].add(key)

        # Generate complete date series for last N days
        daily_metrics: List[DailyViewMetric] = []
        for i in range(days - 1, -1, -1):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            if day in daily_data:
                daily_metrics.append(
                    DailyViewMetric(
                        date=day,
                        views=daily_data[day]["views"],
                        unique_views=len(daily_data[day]["unique_keys"]),
                    )
                )
            else:
                daily_metrics.append(
                    DailyViewMetric(
                        date=day,
                        views=0,
                        unique_views=0,
                    )
                )

        return ProjectAnalyticsResponse(
            project_id=project_id,
            total_views=total_views,
            unique_viewers=unique_viewers,
            daily_views=daily_metrics,
        )

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.dependencies import get_database
from app.models.project import Project
from app.models.user import User
from app.models.organization import Organization
from app.models.skill import Skill
from app.models.project_skill import ProjectSkill
from app.models.user_skill import UserSkill
from app.models.project_member import ProjectMember
from app.models.organization_member import OrganizationMember
from app.middleware.rate_limit import limiter

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("/dependencies")
@limiter.limit("30/minute")
def get_dependency_graph(
    request: Request,
    db: Session = Depends(get_database),
    limit: int = Query(50, le=200),
):
    nodes = []
    edges = []

    # Helper to add node if not exists
    node_ids = set()

    def add_node(id_str, label, type_name):
        if id_str not in node_ids:
            nodes.append(
                {
                    "id": id_str,
                    "data": {"label": label, "type": type_name},
                    "type": type_name,
                }
            )
            node_ids.add(id_str)

    # 1. Projects and their required skills
    projects = db.query(Project).limit(limit).all()
    for p in projects:
        p_id = f"proj_{p.id}"
        add_node(p_id, p.name, "project")

        # Project -> Skills
        for ps in db.query(ProjectSkill).filter(ProjectSkill.project_id == p.id).all():
            skill = db.query(Skill).filter(Skill.id == ps.skill_id).first()
            if skill:
                s_id = f"skill_{skill.id}"
                add_node(s_id, skill.name, "skill")
                edges.append(
                    {
                        "id": f"e_{p_id}_{s_id}",
                        "source": p_id,
                        "target": s_id,
                        "label": "requires",
                        "type": "default",
                    }
                )

        # Project -> Members (Users)
        for pm in (
            db.query(ProjectMember).filter(ProjectMember.project_id == p.id).all()
        ):
            user = db.query(User).filter(User.id == pm.user_id).first()
            if user:
                u_id = f"user_{user.id}"
                add_node(u_id, user.username, "user")
                edges.append(
                    {
                        "id": f"e_{u_id}_{p_id}",
                        "source": u_id,
                        "target": p_id,
                        "label": (
                            pm.role.value if hasattr(pm.role, "value") else str(pm.role)
                        ),
                        "type": "default",
                    }
                )

    # 2. Users and their skills
    users = db.query(User).limit(limit).all()
    for u in users:
        u_id = f"user_{u.id}"
        add_node(u_id, u.username, "user")
        for us in db.query(UserSkill).filter(UserSkill.user_id == u.id).all():
            skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
            if skill:
                s_id = f"skill_{skill.id}"
                add_node(s_id, skill.name, "skill")
                edges.append(
                    {
                        "id": f"e_{u_id}_{s_id}",
                        "source": u_id,
                        "target": s_id,
                        "label": "knows",
                        "type": "default",
                    }
                )

    # 3. Organizations and their members
    orgs = db.query(Organization).limit(limit).all()
    for o in orgs:
        o_id = f"org_{o.id}"
        add_node(o_id, o.name, "organization")

        for om in (
            db.query(OrganizationMember)
            .filter(OrganizationMember.organization_id == o.id)
            .all()
        ):
            user = db.query(User).filter(User.id == om.user_id).first()
            if user:
                u_id = f"user_{user.id}"
                add_node(u_id, user.username, "user")
                edges.append(
                    {
                        "id": f"e_{u_id}_{o_id}",
                        "source": u_id,
                        "target": o_id,
                        "label": "member",
                        "type": "default",
                    }
                )

    return {"nodes": nodes, "edges": edges}

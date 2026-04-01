from sqlalchemy import func, or_, case

from models.problem.problem import Problem
from models.problem.problem_tag import ProblemTag
from models.problem.problem_react import ProblemReact
from models.submission.submission import Submission
from models.user.user import User
from models.message.message import Message
from models.message.message_context import MessageContext

from models.enums import ReactionType, SubmissionStatus, MessageContextType

class ProblemRepository:
    # LIST BASE
    def list_problems(self, session, query=None, tags=None):
        q = session.query(Problem)

        if query:
            search = f"%{query}%"
            q = q.join(User).filter(
                or_(
                    User.name.ilike(search),
                    User.nickname.ilike(search),
                    Problem.title.ilike(search),
                    Problem.description.ilike(search)
                )
            )

        if tags:
            q = q.join(ProblemTag).filter(ProblemTag.tag.in_(tags))

        return q.distinct().all()

    # REACTIONS
    def get_reactions_count(self, session, problem_ids):
        rows = session.query(
            ProblemReact.problem_id,
            ProblemReact.reaction,
            func.count().label("count")
        ).filter(
            ProblemReact.problem_id.in_(problem_ids)
        ).group_by(
            ProblemReact.problem_id,
            ProblemReact.reaction
        ).all()

        result = {pid: {"likes": 0, "dislikes": 0} for pid in problem_ids}

        for r in rows:
            if r.reaction == ReactionType.LIKE:
                result[r.problem_id]["likes"] = r.count
            
            elif r.reaction == ReactionType.DISLIKE:
                result[r.problem_id]["dislikes"] = r.count

        return result

    # TAGS
    def get_tags(self, session, problem_ids):
        rows = session.query(
            ProblemTag.problem_id,
            ProblemTag.tag
        ).filter(
            ProblemTag.problem_id.in_(problem_ids)
        ).all()

        result = {pid: [] for pid in problem_ids}

        for r in rows:
            result[r.problem_id].append(r.tag)

        return result

    # SUBMISSIONS
    def get_submission_stats_bulk(self, session, problem_ids):
        rows = session.query(
            Submission.problem_id,

            # total
            func.count().label("total"),

            # accepted
            func.sum(
                case(
                    (Submission.status == SubmissionStatus.ACCEPTED, 1),
                    else_=0
                )
            ).label("accepted")

        ).filter(
            Submission.problem_id.in_(problem_ids)
        ).group_by(
            Submission.problem_id
        ).all()

        result = {
            pid: {"total": 0, "accepted": 0}
            for pid in problem_ids
        }

        for r in rows:
            result[r.problem_id] = {
                "total": r.total,
                "accepted": r.accepted
            }

        return result
    
    # PROBLEM BASE INFO
    def get_problem_by_id(self, session, problem_id):
        return session.query(Problem).filter(
            Problem.problem_id == problem_id
        ).first()

    # CREATOR
    def get_creator_name(self, session, creator_id):
        user = session.query(User).filter(
            User.user_id == creator_id
        ).first()

        return user.name if user else None

    # REACTIONS
    def get_reactions(self, session, problem_id):

        rows = session.query(
            ProblemReact.reaction,
            func.count().label("count")
        ).filter(
            ProblemReact.problem_id == problem_id
        ).group_by(
            ProblemReact.reaction
        ).all()

        result = {"likes": 0, "dislikes": 0}

        for r in rows:
            if r.reaction == ReactionType.LIKE:
                result["likes"] = r.count
            elif r.reaction == ReactionType.DISLIKE:
                result["dislikes"] = r.count

        return result


    # SUBMISSIONS
    def get_submission_stats_single(self, session, problem_id):

        row = session.query(
            func.count().label("total"),
            func.sum(
                case(
                    (Submission.status == SubmissionStatus.ACCEPTED, 1),
                    else_=0
                )
            ).label("accepted")
        ).filter(
            Submission.problem_id == problem_id
        ).first()

        return {
            "total": row.total or 0,
            "accepted": row.accepted or 0
        }

    # TAGS
    def get_problem_tags(self, session, problem_id):
        rows = session.query(
            ProblemTag.tag
        ).filter(
            ProblemTag.problem_id == problem_id
        ).all()

        return [r.tag for r in rows]

    # COMMENTS
    def get_comments(self, session, problem_id):
        rows = session.query(
            Message.message_id,
            Message.message,
            Message.sent_at,
            User.name,
            User.user_id,
            User.avatar,
        ).join(
            MessageContext,
            MessageContext.message_id == Message.message_id
        ).join(
            User,
            User.user_id == Message.user_id
        ).filter(
            MessageContext.context_type == MessageContextType.PROBLEM,
            MessageContext.context_ref_id == problem_id
        ).order_by(
            Message.sent_at.desc()
        ).all()

        return [
            {
                "message": r.message,
                "user_name": r.name,
                "user_id": r.user_id,
                "user_avatar": r.avatar,
                "sent_at": r.sent_at,
            }
            for r in rows
        ]
    
    def get_user_reaction(self, session, problem_id, user_id):
        react = session.query(ProblemReact).filter(
            ProblemReact.problem_id == problem_id,
            ProblemReact.user_id == user_id
        ).first()

        if not react:
            return None

        return react.reaction.value  # "LIKE" | "DISLIKE"
    
    def upsert_problem_react(self, session, problem_id, user_id, react_type: ReactionType):
        existing = session.query(ProblemReact).filter(
            ProblemReact.problem_id == problem_id,
            ProblemReact.user_id == user_id
        ).first()

        # Já existe
        if existing:
            # Mesmo tipo → remove (toggle)
            if existing.reaction == react_type:
                session.delete(existing)
                return "removed"

            # Tipo diferente → atualiza
            existing.reaction = react_type
            return "updated"

        # Não existe
        session.add(
            ProblemReact(
                problem_id=problem_id,
                user_id=user_id,
                reaction=react_type
            )
        )
        return "created"
    
    def count_problems(self, session):
        return session.query(func.count(Problem.problem_id)).scalar()
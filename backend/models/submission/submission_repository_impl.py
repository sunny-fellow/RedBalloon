from models.submission.submission_repository import SubmissionRepository
from models.submission.submission import Submission
from models.submission.submission_react import SubmissionReact
from models.enums import SubmissionStatus

class SQLAlchemySubmissionRepository(SubmissionRepository):
    def save_submission(self, session, problem_id, user_id, code, language, time_spent, status, submitted_at):
        sub = Submission(
            problem_id=problem_id,
            user_id=user_id,
            code=code,
            language=language,
            time_spent=time_spent,
            status=SubmissionStatus[status],
            submitted_at=submitted_at
        )
        session.add(sub)
        session.flush()  # Garante que tem ID
        return sub

    def get_accepted_submissions(self, session, problem_id):
        return (
            session.query(Submission)
            .filter_by(problem_id=problem_id, status=SubmissionStatus.ACCEPTED)
            .all()
        )

    def get_submission(self, session, submission_id):
        return session.get(Submission, submission_id)

    def get_existing_react(self, session, submission_id, user_id):
        return (
            session.query(SubmissionReact)
            .filter_by(submission_id=submission_id, user_id=user_id)
            .first()
        )

    def add_react(self, session, submission_id, user_id, reaction):
        react = SubmissionReact(
            submission_id=submission_id,
            user_id=user_id,
            reaction=reaction
        )
        session.add(react)
        return react

    def remove_react(self, session, react):
        session.delete(react)

    def update_react(self, react, reaction):
        react.reaction = reaction

    def get_submission_details(self, session, submission_id, requesting_user_id):
        sub: Submission = session.get(Submission, submission_id)
        if not sub:
            return None

        likes = sum(1 for r in sub.reacts if r.reaction.value == "LIKE")
        dislikes = sum(1 for r in sub.reacts if r.reaction.value == "DISLIKE")

        # Reação do usuário que requisitou
        user_react = next(
            (r.reaction.value for r in sub.reacts if r.user_id == requesting_user_id),
            None
        )

        return {
            "submission_id": sub.submission_id,
            "time_spent": sub.time_spent,
            "memory_used": sub.memory_used,
            "creator_id": sub.user_id,
            "creator_name": sub.user.name,
            "creator_avatar": sub.user.avatar,
            "code": sub.code,
            "language": sub.language.value,
            "likes": likes,
            "dislikes": dislikes,
            "user_reaction": user_react,
            "problem_id": sub.problem.problem_id,
            "problem_title": sub.problem.title,
            "problem_creator_name": sub.problem.creator.name,
            "problem_description": sub.problem.description,
            "problem_difficulty": sub.problem.difficulty,
            "problem_tags": [t.name for t in sub.problem.tags]
        }
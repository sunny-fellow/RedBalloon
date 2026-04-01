from models.factories.sqlalchemy_factory import SQLAlchemyRepositoryFactory
from database.service import DatabaseService
from utils.singleton import Singleton
from utils.app_error import AppError
from submission.validators.submit import SubmissionValidator
from execution.service import ExecutionService
from datetime import datetime, timezone


@Singleton
class SubmissionService:
    def __init__(self):
        self.db_service = DatabaseService()
        factory = SQLAlchemyRepositoryFactory()
        self.repository = factory.create_submission_repository()
        self.executor = ExecutionService(self.db_service)

    def submit(self, data):
        SubmissionValidator().validate(data)

        user_id = data["user_id"]
        problem_id = data["problem_id"]
        language = data["language"]
        source_code = data["source_code"]

        exec_res = self.executor.run(
            problem_id=problem_id,
            source_code=source_code,
            language=language
        )

        status = exec_res.get("status", "JUDGING")
        if status not in ["ACCEPTED", "WRONG_ANSWER", "VERIFICATION_ERROR",
                          "TIME_LIMIT_EXCEEDED", "MEMORY_LIMIT_EXCEEDED",
                          "RUNTIME_ERROR", "COMPILATION_ERROR"]:
            status = "JUDGING"

        def _save(session):
            sub = self.repository.save_submission(
                session=session,
                problem_id=problem_id,
                user_id=user_id,
                code=source_code,
                language=language,
                time_spent=exec_res.get("time_spent"),
                status=status,
                submitted_at=datetime.now(timezone.utc).isoformat()
            )
            return {"submission": sub, "status": status, **exec_res}

        return self.db_service.run(_save, user_id=user_id)

    def problem_submissions(self, problem_id):
        def _query(session):
            subs = self.repository.get_accepted_submissions(session, problem_id)

            result = []
            for s in subs:
                likes = sum(1 for r in s.reacts if r.reaction.value == "LIKE")
                dislikes = sum(1 for r in s.reacts if r.reaction.value == "DISLIKE")

                result.append({
                    "submission_id": s.submission_id,
                    "problem_id": s.problem_id,
                    "user_id": s.user_id,
                    "user_name": s.user.name,
                    "user_avatar": s.user.avatar,
                    "status": s.status.value,
                    "submitted_at": s.submitted_at,
                    "likes": likes,
                    "dislikes": dislikes,
                    "time_spent": s.time_spent
                })

            result.sort(key=lambda x: x["likes"], reverse=True)
            return result

        return self.db_service.run(_query)

    def react(self, data):
        user_id = data["user_id"]
        submission_id = data["submission_id"]
        reaction = data["reaction"].upper()

        if reaction not in ["LIKE", "DISLIKE"]:
            raise AppError("Invalid reaction type")

        def _execute(session):
            sub = self.repository.get_submission(session, submission_id)
            if not sub:
                raise AppError("Submission not found")

            existing = self.repository.get_existing_react(session, submission_id, user_id)

            if existing:
                if existing.reaction.value == reaction:
                    self.repository.remove_react(session, existing)
                    return {"status": "REMOVED"}
                else:
                    self.repository.update_react(existing, reaction)
                    return {"status": "UPDATED"}

            self.repository.add_react(session, submission_id, user_id, reaction)
            return {"status": "CREATED"}

        return self.db_service.run(_execute)
    
    def details(self, data):
        submission_id = data["submission_id"]
        user_id = data["user_id"]

        def _query(session):
            details = self.repository.get_submission_details(session, submission_id, user_id)
            if not details:
                raise AppError("Submission not found", 404)
            
            return details

        return self.db_service.run(_query, user_id=user_id)
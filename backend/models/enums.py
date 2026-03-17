from enum import Enum

class ProblemDifficulty(str, Enum):
    BEGGINNER = "BEGGINNER"
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class RoomStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CROWDED = "CROWDED"


class SubmissionStatus(str, Enum):
    JUDGING = "JUDGING"
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    VERIFICATION_ERROR = "VERIFICATION_ERROR"


class LanguageType(str, Enum):
    PYTHON = "PYTHON"
    C = "C"
    CPP = "CPP"
    JAVA = "JAVA"

class TagType(str, Enum):
    PROBLEM = "PROBLEM"
    MESSAGE = "MESSAGE"

class MessageContextType(str, Enum):
    GLOBAL = "GLOBAL"
    PROBLEM = "PROBLEM"
    SOLUTION = "SOLUTION"

class ValidationMode(str, Enum):
    INPUTS_OUTPUTS = "INPUTS_OUTPUTS"
    CHECKER_ALGORITHM = "CHECKER_ALGORITHM"
    NO_VALIDATION = "CHECKER_ALGORITHM"

class ReactionType(str, Enum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
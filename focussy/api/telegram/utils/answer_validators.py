from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, answer: str, correct_answer: str):
        pass


class TextValidator(Validator):
    def validate(self, answer: str, correct_answer: str):
        return len(correct_answer) == len(answer) and all(
            (a in answer) for a in correct_answer
        )


class NumUnorderedValidator(Validator):
    def validate(self, answer: str, correct_answer: str):
        return len(correct_answer) == len(answer) and all(
            (a in answer) for a in correct_answer
        )


class NumOrderedValidator(Validator):
    def validate(self, answer: str, correct_answer: str):
        return answer == correct_answer


class AnswerValidator:
    validators: dict[str, Validator] = {
        "text": TextValidator(),
        "num_unordered": NumUnorderedValidator(),
        "num_ordered": NumOrderedValidator(),
    }

    @staticmethod
    def validate(task_type: str, answer: str, correct_answer: str):
        return len(answer) > 0 and AnswerValidator.validators[task_type].validate(
            answer, correct_answer
        )

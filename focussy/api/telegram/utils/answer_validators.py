from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, answer: str, correct_answer: str):
        pass


class TextValidator(Validator):
    def validate(self, answer: str, correct_answer: str):
        return answer.lower() == correct_answer.lower()


class NumUnorderedValidator(Validator):
    def validate(self, answer: str, correct_answer: str):
        return all((a in correct_answer) for a in answer)


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
        return AnswerValidator.validators[task_type].validate(answer, correct_answer)


if __name__ == "__main__":
    print(AnswerValidator.validate("num_unordered", "21", "1,2"))

from assignment.models import Assignment, AssignmentSubmission


class AssigmentProxy(Assignment):
    class Meta:
        proxy = True
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class AssigmentSubmissionProxy(AssignmentSubmission):
    class Meta:
        proxy = True
        verbose_name = "Сдача задания"
        verbose_name_plural = "Сдачи заданий"
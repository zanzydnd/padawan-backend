from datetime import timedelta

from assignment.models import AssignmentSubmission, AlgSubmissionResults, ApiSubmissionResults
from padawan.celery_farmer import celery_app
from testing.models import StepValidator
from testing.utils import scenario_db_to_dict


@celery_app.task(name="web.send_submission")
def send_submission(submission_id: int):
    submission = AssignmentSubmission.objects.filter(id=submission_id).select_related("assignment") \
        .prefetch_related("assignment__api_scenarios", "assignment__alg_scenarios", "assignment__api_scenarios",
                          "assignment__api_scenarios__steps", "assignment__alg_scenarios__steps",
                          "assignment__static_analysis_blocks",
                          ).first()
    to_send = {
        "submission_id": submission.id,
        "scenarios": [],
        "git_url": submission.git_url
    }
    if submission.assignment.assigment_type == submission.assignment.Type.api:
        to_send["scenarios"] = [
            {**scenario_db_to_dict(scenario), "id": scenario.id}
            for scenario in submission.assignment.api_scenarios.all()
        ]
        celery_app.send_task('remote.test_api_submission', kwargs=to_send)
    else:
        to_send["scenarios"] = [
            {
                "name": scenario.name,
                "id": scenario.id,
                "steps": [
                    {
                        "input": step.input,
                        "expected": step.expected,
                        "time": step.time.seconds,
                        "id": step.id
                    }
                    for step in scenario.steps.all()
                ]
            }
            for scenario in submission.assignment.alg_scenarios.all()
        ]
        celery_app.send_task('remote.test_alg_submission', kwargs=to_send)

    if submission.assignment.static_analysis_blocks.exists():
        analysis_kwargs = {
            "submission_id": submission.id,
            "git_url": submission.git_url,
            "analysis_steps": submission.assignment.static_analysis_blocks.all().values_list("name", flat=True)
        }

        celery_app.send_task('remote.static_analysis', kwargs=analysis_kwargs)


def _process_submission_alg(submission: AssignmentSubmission, data: dict):
    for scenario_id in data.get("scenarios").keys():
        for step_id in data.get("scenarios").get(scenario_id).keys():
            step_data = data.get("scenarios").get(scenario_id).get(step_id)
            AlgSubmissionResults.objects.create(
                submission=submission,
                step_id=step_id,
                success=step_data.get("time").get("success"),
                time=timedelta(seconds=step_data.get("time").get("actual")),
            )
            AlgSubmissionResults.objects.create(
                submission=submission,
                step_id=step_id,
                success=step_data.get("comparison").get("success"),
                actual=step_data.get("comparison").get("actual"),
            )


def _process_submission_api(submission: AssignmentSubmission, data: dict):
    for scenario_id in data.get("scenarios").keys():
        scenario_data = data.get("scenarios").get(scenario_id)
        for test_name in scenario_data.keys():
            test_data = scenario_data.get(test_name)
            for validator_results in test_data:
                if validator_results == "-":
                    for validator in StepValidator.objects.filter(step__scenario_id=scenario_id, step__name=test_name):
                        ApiSubmissionResults.objects.create(
                            submission=submission,
                            validator=validator,
                            success=False,
                            message="Необходимо поправить предыдущие шаги.",
                        )
                    continue
                ApiSubmissionResults.objects.create(
                    submission=submission,
                    validator_id=validator_results.get("id"),
                    success=validator_results.get("success"),
                    message=validator_results.get("message"),
                    status=validator_results.get("status"),
                    headers=validator_results.get("headers"),
                    body=validator_results.get("body"),
                )


@celery_app.task(name="web.process_submission_result")
def process_submission_result(data: dict):
    print(data)
    submission = AssignmentSubmission.objects.filter(id=data.get("submission_id")) \
        .select_related("assignment", ) \
        .prefetch_related("assignment__api_scenarios", "assignment__alg_scenarios", "assignment__api_scenarios__steps",
                          "assignment__api_scenarios__steps__validators", "assignment__alg_scenarios__steps", "results",
                          "results__validator") \
        .first()

    if submission.assignment.assigment_type == submission.assignment.Type.api:
        _process_submission_api(submission, data)
    else:
        _process_submission_alg(submission, data)

    submission.status = "Проверено"
    submission.save()


@celery_app.task(name="web.process_submission_result_analysis")
def process_submission_result_analysis(data: dict, submission_id: int):
    pass

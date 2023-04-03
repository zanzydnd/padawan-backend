from assignment.models import AssignmentSubmission
from padawan.celery_farmer import celery_app
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

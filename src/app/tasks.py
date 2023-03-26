from assignment.models import AssignmentSubmission
from padawan.celery_farmer import celery_app
from testing.utils import scenario_db_to_dict


@celery_app.task(name="web.send_submission")
def send_submission(submission_id: int, file_path: str = None, github_url: str = None):
    submission = AssignmentSubmission.objects.filter(id=submission_id).select_related("assignment") \
        .prefetch_related("assignment__api_scenarios", "assignment__alg_scenarios", "assignment__api_scenarios",
                          "assignment__api_scenarios__steps", "assignment__alg_scenarios__steps",
                          ).first()
    to_send = {
        "submission_id": submission.id,
        "scenarios": []
    }
    if submission.assignment.assigment_type == submission.assignment.Type.api:
        to_send["scenarios"] = [
            scenario_db_to_dict(scenario)
            for scenario in submission.assignment.api_scenarios.all()
        ]
        to_send["git_url"] = github_url
        print()
        celery_app.send_task('remote.test_api_submission', kwargs=to_send)
    else:
        celery_app.send_task('remote.test_alg_submission', kwargs=to_send)

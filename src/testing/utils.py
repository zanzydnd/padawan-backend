import json
import re
from pprint import pprint
from typing import List, Union, Optional
from ast import literal_eval

from django.core.files.uploadedfile import UploadedFile
from ruamel import yaml

from testing.models import Scenario, Step, StepValidator
from padawan.exceptions import ImportingFileException, ScenarioValidationError


def imported_file_to_dict(file: UploadedFile) -> dict:
    if file.name.endswith(".yaml") or file.name.endswith(".yml"):
        return yaml.safe_load(file)

    return json.loads(file.read())


def _check_error_in_template_var(string: str, test_names: set) -> Optional[str]:
    """
        Returns wrong referenced test name or None if nothing wrong
    """
    for template_var_usage in re.findall("\${.*}", string):
        ref_test_name = template_var_usage.strip("${").strip("}").split(":")[0]
        if ref_test_name not in test_names:
            return ref_test_name


def validate_imported_scenario_dict(imported: dict):
    tests = imported.get("tests")
    if not tests: raise ScenarioValidationError("Отсутствуют тесты.")
    if not imported.get("name"): raise ScenarioValidationError("Отсутствует название сценария.")

    tests_name_set = set()
    for test in tests:
        test_points_sum = 0
        test_name = test.get("name")
        body = test.get("body")
        url = test.get("url")

        headers = test.get("headers")
        if not headers:
            raise ScenarioValidationError(f"Определите заголовки у теста '{test_name}'")

        try:
            headers = json.loads(headers)
        except Exception as e:
            raise ScenarioValidationError(f"Невалидные заголовки у теста '{test_name}'")

        if test_name in tests_name_set:
            raise ScenarioValidationError("Существуют тесты с одинаковым названием.")
        if ' ' in test_name or ':' in test_name:
            raise ScenarioValidationError("Название теста не должно содержать пробелы или ':'.")

        tests_name_set.add(test.get("name"))

        if body:
            if ref_test_name := _check_error_in_template_var(body, tests_name_set):
                raise ScenarioValidationError(f"Тест: '{test_name}' ссылается на тест '{ref_test_name}, "
                                              f"который не воспроизводился.'")

        if url:
            if ref_test_name := _check_error_in_template_var(url, tests_name_set):
                raise ScenarioValidationError(f"Тест: '{test_name}' ссылается на тест '{ref_test_name}, "
                                              f"который не воспроизводился.'")

        for validator in test.get("validators", []):
            if not validator.get("points"):
                raise ScenarioValidationError(f"Шаг: '{test_name}' не проставлено кол-во баллов в валидаторе.")
            test_points_sum += validator.get("points")

            if "compare" in validator.keys():
                comparator = validator.get("compare")
                expected = comparator.get("expected")
                actual = comparator.get("actual")

                if not expected:
                    raise ScenarioValidationError("Не указан ожидаемый результат.")

                if ref_test_name := _check_error_in_template_var(expected, tests_name_set):
                    raise ScenarioValidationError(f"Тест: '{test_name}' ссылается на тест '{ref_test_name}, "
                                                  f"который не воспроизводился.'")

                if actual:
                    if ref_test_name := _check_error_in_template_var(actual, tests_name_set):
                        raise ScenarioValidationError(f"Тест: '{test_name}' ссылается на тест '{ref_test_name}, "
                                                      f"который не воспроизводился.'")

        if headers:
            for header_val in headers.values():
                if ref_test_name := _check_error_in_template_var(header_val, tests_name_set):
                    raise ScenarioValidationError(f"Тест: '{test_name}' ссылается на тест '{ref_test_name}, "
                                                  f"который не воспроизводился.'")


def scenario_dict_to_scenario_db(imported: dict) -> tuple[Scenario, List[Step]]:
    try:
        validate_imported_scenario_dict(imported)
    except ScenarioValidationError as e:
        raise ImportingFileException(str(e))

    scenario = Scenario(
        name=imported.get("name"),
        max_points=(imported.get("max_points") if imported.get("max_points") else 0)
    )
    scenario.save()
    print(imported)
    steps_in_order = []
    for i, step in enumerate(imported.get("tests")):
        print(f"{step.get('name')} {i}")
        validators = step.pop("validators")
        step_db = Step(**step, scenario=scenario)
        step_db.save()
        for validator_dct in validators:
            StepValidator.objects.create(
                step=step_db,
                **validator_dct
            )
        steps_in_order.append(step_db)

    return scenario, steps_in_order


def scenario_db_to_dict(scenario: Scenario) -> dict:
    result = {
        "name": scenario.name,
        "max_points": scenario.max_points,
        "tests": []
    }

    scenario_steps = Step.objects.filter(scenario=scenario).prefetch_related("validators")

    for step in scenario_steps:
        validators = [
            {
                "allowed_response_statuses": validator.allowed_response_statuses,
                "expected_response_body": validator.expected_response_body,
                "timeout": validator.timeout,
                "points": validator.points,
                "id": validator.id
            }
            for validator in step.validators.all()
        ]
        result.get("tests").append(
            {
                "method": step.method,
                "url": step.url,
                "name": step.name,
                "body": step.body,
                "headers": step.headers,
                "validators": validators
            }
        )

    return result

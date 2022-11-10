import json

from django_celery_beat.models import ClockedSchedule, PeriodicTask


def create_task_schedule(
    name: str, start_time, arguments: dict, celery_task_name: str
) -> None:
    """utils for create all tasks
    REMEMBER: try to DRY
    """
    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=start_time)
    new_celery_task = PeriodicTask.objects.update_or_create(
        name=name,
        defaults={
            "task": f"api.tasks.{celery_task_name}",
            "kwargs": json.dumps(arguments),
            "one_off": True,
            "clocked": clocked,
        },
    )

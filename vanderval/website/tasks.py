import logging
from time import sleep, time
from website.models import Site, UserRecords, Tasks
from celery import shared_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handle_task_failure(task_id, start_time, exception):
    """
    Handles task failure by updating task status and logging the error.
    """
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.FAILED
        task.failure_reason = str(exception)
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()
        logger.error("Task {} failed: {}".format(task_id, str(exception)))
    except Exception as e:
        logger.error("Error while handling failure for task {}: {}".format(task_id, str(e)))

@shared_task
def task_01(site_id: int, task_id: int):
    start_time = time()
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.IN_PROGRESS
        task.save()

        TIME_MULTIPLIER = 0.001
        site = Site.objects.get(id=site_id)
        records = UserRecords.objects.filter(site=site, is_active=True)
        for record in records:
            sleep(TIME_MULTIPLIER)
            logger.info("Task 01: {} processed".format(record.name))

        task.status = Tasks.COMPLETED
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()

    except Exception as exception:
        handle_task_failure(task_id, start_time, exception)
        return False
    return True

@shared_task
def task_02(site_id: int, task_id: int):
    start_time = time()
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.IN_PROGRESS
        task.save()

        TIME_MULTIPLIER = 0.01
        site = Site.objects.get(id=site_id)
        records = UserRecords.objects.filter(site=site, is_active=True)
        for record in records:
            sleep(TIME_MULTIPLIER)
            logger.info("Task 02: {} processed".format(record.name))

        task.status = Tasks.COMPLETED
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()

    except Exception as exception:
        handle_task_failure(task_id, start_time, exception)
        return False
    return True

@shared_task
def task_03(site_id: int, task_id: int):
    start_time = time()
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.IN_PROGRESS
        task.save()

        TIME_MULTIPLIER = 0.1
        site = Site.objects.get(id=site_id)
        records = UserRecords.objects.filter(site=site, is_active=True)
        for record in records:
            sleep(TIME_MULTIPLIER)
            logger.info("Task 03: {} processed".format(record.name))

        task.status = Tasks.COMPLETED
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()

    except Exception as exception:
        handle_task_failure(task_id, start_time, exception)
        return False
    return True

@shared_task
def task_04(site_id: int, task_id: int):
    start_time = time()
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.IN_PROGRESS
        task.save()

        TIME_MULTIPLIER = 1
        site = Site.objects.get(id=site_id)
        records = UserRecords.objects.filter(site=site, is_active=True)
        for record in records:
            sleep(TIME_MULTIPLIER)
            logger.info("Task 04: {} processed".format(record.name))

        task.status = Tasks.COMPLETED
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()

    except Exception as exception:
        handle_task_failure(task_id, start_time, exception)
        return False
    return True

@shared_task
def task_05(site_id: int, task_id: int):
    start_time = time()
    try:
        task = Tasks.objects.get(id=task_id)
        task.status = Tasks.IN_PROGRESS
        task.save()

        TIME_MULTIPLIER = 10
        site = Site.objects.get(id=site_id)
        records = UserRecords.objects.filter(site=site, is_active=True)
        for record in records:
            sleep(TIME_MULTIPLIER)
            logger.info("Task 05: {} processed".format(record.name))

        task.status = Tasks.COMPLETED
        end_time = time()
        task.execution_time = int(end_time - start_time)
        task.save()

    except Exception as exception:
        handle_task_failure(task_id, start_time, exception)
        return False
    return True


task_map = {
            "task_01": task_01,
            "task_02": task_02,
            "task_03": task_03,
            "task_04": task_04,
            "task_05": task_05,
        }
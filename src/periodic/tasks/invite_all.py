from celery.utils.log import get_task_logger
from django.db.models import Q

from periodic import tasks
from periodic.app import app
from periodic.utils.xmodels import get_auth_profile_model

logger = get_task_logger(__name__)


@app.task
def invite_all_users():
    logger.debug(f"starting invites")

    auth_profile_model = get_auth_profile_model()
    criteria = Q(verified_at__isnull=True) & Q(notified_at__isnull=True)
    auth_profiles = auth_profile_model.objects.filter(criteria)

    logger.debug(f"nr auth profiles to process: {auth_profiles.count()}")

    emails = {_prof.user.email for _prof in auth_profiles}

    for email in emails:
        tasks.invite_single_user.delay(email)
        logger.debug(f"invite to process: {email}")

    logger.debug("done")

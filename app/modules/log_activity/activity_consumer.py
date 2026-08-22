import json
import logging

from app.core.config import settings
from app.modules.log_activity.service import ActivityLogService


logger = logging.getLogger(__name__)


async def activity_consumer(redis, db):
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.ACTIVITY_CHANNEL)

    logger.info("ACTIVITY CONSUMER STARTED")
    logger.info(f"Channel: {settings.ACTIVITY_CHANNEL}")


    activity_service = ActivityLogService(db)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])

            event_name = data["event"]
            payload = data["payload"]

            logger.info("========== NEW ACTIVITY ==========")
            logger.info(f"Event: {event_name}")
            logger.info(f"User: {payload.get('user_id')}")
            logger.info(f"Project: {payload.get('project_id')}")
            logger.info(f"Target: {payload.get('target_id')}")
            logger.info("==================================")

            await activity_service.create_log(
                user_id=payload["user_id"],
                action=event_name,
                project_id=payload.get("project_id"),
                target_id=payload.get("target_id"),
            )

            await db.commit()

            logger.info("Activity saved to database")

        except Exception:
            logger.exception("Activity failed to process message")
            await db.rollback()
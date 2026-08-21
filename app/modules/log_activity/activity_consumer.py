import json
import logging

from app.core.config import settings
from app.modules.log_activity.service import ActivityLogService


logger = logging.getLogger(__name__)


async def activity_consumer(redis, db):
    pubsub = redis.pubsub()
    await pubsub.subscribe(settings.ACTIVITY_CHANNEL)

    logger.info("Activity consumer started")
    activity_service = ActivityLogService(db)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])
            event_name = data["event"]
            payload = data["payload"]

            logger.info(f"[ACTIVITY] {event_name} -> {payload}")

            await activity_service.create_log(
                user_id=payload["user_id"],
                action=event_name,
                project_id=payload.get("project_id"),
                target_id=payload.get("target_id"),
            )
            await db.commit()

        except Exception:
            logger.exception("[ACTIVITY] failed to process message")
            await db.rollback()
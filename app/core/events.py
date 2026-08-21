import json
import logging
from app.core.config import settings
logger = logging.getLogger(__name__)


async def publish_event(redis, event_name: str, payload: dict):
    event = {
        "event": event_name,
        "payload": payload,
    }

    logger.info(f"[EVENT] {event_name}")

    await redis.publish(
        settings.ACTIVITY_CHANNEL,
        json.dumps(event),
    )
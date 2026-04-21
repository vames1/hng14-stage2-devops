import redis
import time
import os
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True
)

running = True


def handle_shutdown(signum, frame):
    global running
    logger.info("Shutdown signal received. Stopping worker...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    try:
        logger.info(f"Processing job {job_id}")
        r.hset(f"job:{job_id}", "status", "processing")
        time.sleep(2)
        r.hset(f"job:{job_id}", "status", "completed")
        logger.info(f"Done: {job_id}")
    except Exception as e:
        logger.error(f"Failed to process job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


logger.info("Worker started. Waiting for jobs...")

while running:
    try:
        job = r.brpop("jobs", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)
    except Exception as e:
        logger.error(f"Redis error: {e}")
        time.sleep(2)

logger.info("Worker stopped cleanly.")

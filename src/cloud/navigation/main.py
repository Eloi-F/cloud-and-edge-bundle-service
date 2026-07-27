import threading
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import PORT
from app.api.routes import router
from app.discovery.policy_manager import PolicyManager
from app.discovery.watcher import start_policy_watcher
from app.discovery.sender import send_periodically


@asynccontextmanager
async def lifespan(_: FastAPI):
    PolicyManager.reload_odrl()

    stop_event = threading.Event()
    worker_thread = threading.Thread(
        target=send_periodically,
        args=(stop_event,),
        daemon=True,
    )
    worker_thread.start()

    observer = start_policy_watcher()

    try:
        yield
    finally:
        stop_event.set()
        worker_thread.join(timeout=2)

        observer.stop()
        observer.join()


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

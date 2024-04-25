from fastapi import FastAPI
import uvicorn
from logging_config import logger


app = FastAPI()


@app.get("/")
def index_view():
    logger.info(f"{index_view.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"success": True, "message": "SMS Blast Index"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
    # uvicorn.run(app=app, host="0.0.0.0", port=8000)
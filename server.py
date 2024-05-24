from fastapi import FastAPI, Request
import uvicorn
from src.logs.logging_config import logger
from src.services.ghl_service import ghl_processor


app = FastAPI()


@app.post("/")
def telnyx_webhook(request: Request):
    logger.info("WEBHOOK TRIGGERED")
    telnyx_payload = request.json()

    result = ghl_processor(telnyx_payload)
    if result:
        return {"status": "Success", "message": "Inbound message created successfuly"}
    else:
        return {"status": "Error"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)

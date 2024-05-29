from fastapi import FastAPI, Request
import uvicorn
from src.logs.logging_config import logger
from src.services.ghl_service import GHLService


app = FastAPI()


@app.post("/")
def telnyx_webhook(request: Request):
    logger.info("WEBHOOK TRIGGERED")
    telnyx_payload = request.json()
    ghl_service = GHLService()
    result = ghl_service.ghl_processor(telnyx_payload)
    if result:
        return {"status": "Success", "message": "Inbound message created successfuly"}
    else:
        return {"status": "Error"}


@app.get("/oauth")
def oauth():
    return {"success": "True"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5000)

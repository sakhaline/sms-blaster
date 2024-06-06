from flask import Flask, request, jsonify
from src.logs.logging_config import logger
from src.services.ghl_service_db import GHLService

app = Flask(__name__)


@app.route("/", methods=["POST"])
def ghl_webhook():
    logger.debug(f"WEBHOOK PAYLOAD: \n {request.json}")
    try:
        logger.debug("WEBHOOK TRIGGERED")
        telnyx_payload = request.json
        ghl_service = GHLService()
        result = ghl_service.ghl_processor(telnyx_payload)
        if result:
            return jsonify({"status": "Success", "message": "Inbound message created successfuly"})
        else:
            return jsonify({"status": "Error"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "Error", "message": "Internal Server Error"}), 500


@app.route("/oauth", methods=["GET"])
def oauth():
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from src.services.ghl_api import GHLApi
from src.services.ghl_service_db import GHLService
from src.services.telnyx_service_db import TelnyxService


TELNYX = TelnyxService(limit=1000)
GHL = GHLService()
GHLAPI = GHLApi()


if __name__ == "__main__":
    TELNYX.telnyx_processor()

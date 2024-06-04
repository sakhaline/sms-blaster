import os
import json
from src import DATADIR
from src.services.telnyx_api import TelnyxApi
from src.services.ghl_api import GHLApi
from src.services.ghl_service import GHLService
from src.services.telnyx_service_db import TelnyxService
from src.logs.logging_config import logger
from src.services import CONTACTS_FILE



TELNYX = TelnyxService(start=1, end=100)
GHL = GHLService()
GHLAPI = GHLApi()



if __name__ == "__main__":
    TELNYX.telnyx_processor()
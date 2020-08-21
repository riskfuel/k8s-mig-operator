import os
from dotenv import load_dotenv
load_dotenv()

settings = {
    "DRY_RUN": True if os.getenv("DRY_RUN", "False") == "True" else False,
    "ALLOW_NODE_RESET": True if os.getenv("ALLOW_NODE_RESET", "False") == "True" else False,
}

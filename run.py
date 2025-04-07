import os

import coloredlogs
import uvicorn
from dotenv import load_dotenv

load_dotenv(".env")


## Get App Environment Files
env = os.environ.get("ENV", "development")
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))
log_level = os.environ.get("LOG_LEVEL", "INFO")


## Define Workspace Environment
reload_flag = False
if env == "development":
    reload_flag = True


## Configure coloredlogs
coloredlogs.install(
    level=log_level,
    fmt=r"[%(asctime)s] - %(name)s - P%(process)s - %(levelname)s: %(message)s",
)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload_flag,
        use_colors=True,
    )

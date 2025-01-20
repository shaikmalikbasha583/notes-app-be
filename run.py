import os

import coloredlogs
import uvicorn
from dotenv import load_dotenv

load_dotenv(".env")

## Configure coloredlogs
coloredlogs.install(
    level="INFO",
    fmt=r"[%(asctime)s] - %(name)s - P%(process)s - %(levelname)s: %(message)s",
)

## Get App Environment Files
env = os.environ.get("APP_ENV", "development")
host = os.environ.get("APP_HOST", "0.0.0.0")
port = int(os.environ.get("APP_PORT", 8000))

## Define Workspace Environment
reload_flag = False
if env == "development":
    reload_flag = False

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=reload_flag)

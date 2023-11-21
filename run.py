import os

import coloredlogs
import uvicorn

## Configure coloredlogs
coloredlogs.install(
    level="INFO",
    fmt=r"[%(asctime)s] - %(name)s - P%(process)s - %(levelname)s: %(message)s",
)

## Get App Environment Files
env = os.environ.get("ENV", "development")
host = os.environ.get("HOST", "0.0.0.0")
port = os.environ.get("PORT", 8000)

## Define Workspace Environment
reload_flag = False
if env == "development":
    reload_flag = True

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=reload_flag)

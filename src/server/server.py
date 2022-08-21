import logging
import asyncio
import base64
from datetime import datetime
import json
import os
import shutil
import yaml
import aiohttp_jinja2
import jinja2

from aiohttp import web

from .anchor import (
    AnchorHandle,
    NotReadyException,
    INDY_ROLE_TYPES,
    INDY_TXN_TYPES,
    REGISTER_NEW_DIDS,
    get_genesis_file,
)

from .metrics import generate_metrics

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(int(os.getenv("LOG_LEVEL", "").upper() or logging.INFO))
logging.getLogger('indy.ledger').setLevel(int(os.getenv("LOG_LEVEL", "").upper() or logging.INFO))

PATHS = {"python": shutil.which("python3")}

os.chdir(os.path.dirname(__file__))

LOGGER.info("REGISTER_NEW_DIDS is set to %s", REGISTER_NEW_DIDS)

LEDGER_INSTANCE_NAME = os.getenv("LEDGER_INSTANCE_NAME", "Ledger Browser")
LOGGER.info('LEDGER_INSTANCE_NAME is set to "%s"', LEDGER_INSTANCE_NAME)

WEB_ANALYTICS_SCRIPT = os.getenv("WEB_ANALYTICS_SCRIPT", "")
LOGGER.info(
    "Web analytics are %s", "ENABLED" if not "WEB_ANALYTICS_SCRIPT" else "DISABLED"
)


INFO_SITE_URL = os.getenv("INFO_SITE_URL")
INFO_SITE_TEXT = os.getenv("INFO_SITE_TEXT") or os.getenv("INFO_SITE_URL")

APP = web.Application()
aiohttp_jinja2.setup(APP, loader=jinja2.FileSystemLoader("./static"))

ROUTES = web.RouteTableDef()
TRUST_ANCHOR = AnchorHandle()


@ROUTES.get("/")
@aiohttp_jinja2.template("index.html")
async def index(request):
    return {
        "REGISTER_NEW_DIDS": TRUST_ANCHOR._register_dids,
        "LEDGER_INSTANCE_NAME": LEDGER_INSTANCE_NAME,
        "WEB_ANALYTICS_SCRIPT": WEB_ANALYTICS_SCRIPT,
        "INFO_SITE_TEXT": INFO_SITE_TEXT,
        "INFO_SITE_URL": INFO_SITE_URL,
    }


@ROUTES.get("/favicon.ico")
async def favicon(request):
    return web.FileResponse("static/favicon.ico")


ROUTES.static("/include", "./static/include")


def json_response(data, status=200, **kwargs):
    # FIXME - use aiohttp-cors
    kwargs["headers"] = {"Access-Control-Allow-Origin": "*"}
    kwargs["text"] = json.dumps(data, indent=2, sort_keys=True)
    if "content_type" not in kwargs:
        kwargs["content_type"] = "application/json"
    return web.Response(status=status, **kwargs)


def not_ready():
    return web.json_response(data={"detail": "Not ready"}, status=503)


@ROUTES.get("/status")
async def status(request):
    status = TRUST_ANCHOR.public_config
    if status["ready"] and not status["anonymous"]:
        try:
            status["validators"] = await TRUST_ANCHOR.validator_info()
        except NotReadyException:
            return not_ready()
        except asyncio.CancelledError:
            raise
        except Exception:
            LOGGER.exception("Error retrieving validator info")
            status["validators"] = None
    return json_response(status)

@ROUTES.get("/metrics")
async def metrics(request):
    status = TRUST_ANCHOR.public_config
    if status["ready"] and not status["anonymous"]:
        try:
            validator_info = await TRUST_ANCHOR.validator_info()
            metrics = generate_metrics(validator_info)
        except NotReadyException:
            return not_ready()
        except asyncio.CancelledError:
            raise
        except Exception:
            LOGGER.exception("Error retrieving metrics info")
            metrics = ""
            web.Response(status=503)
    return web.Response(text=metrics)


# Expose genesis transaction for easy connection.
@ROUTES.get("/genesis")
async def genesis(request):
    with open(get_genesis_file(), "r") as content_file:
        genesis = content_file.read()
    return web.Response(text=genesis)

async def boot(app):
    LOGGER.info("Creating trust anchor...")
    init = app["anchor_init"] = app.loop.create_task(TRUST_ANCHOR.open())
    init.add_done_callback(
        lambda _task: LOGGER.info("--- Trust anchor initialized ---")
    )


if __name__ == "__main__":
    logging.getLogger("indy.libindy").setLevel(logging.WARNING)
    APP.add_routes(ROUTES)
    APP.on_startup.append(boot)
    LOGGER.info("Running webserver...")
    PORT = int(os.getenv("PORT", "8000"))
    web.run_app(APP, host="0.0.0.0", port=PORT)

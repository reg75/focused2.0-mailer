import os, logging
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

log = logging.getLogger("mailer.security")


API_KEY_NAME = "X-API-KEY"  # header name shown in Swagger
_api_key_header = APIKeyHeader(name=API_KEY_NAME, scheme_name="ApiKeyAuth", auto_error=False)

def _mask(v: str | None) -> str:
    if not v:
        return "<EMPTY>"
    return f"{v[:4]}...{v[-4:]} (len={len(v)})"

def verify_api_key(api_key: str = Security(_api_key_header)) -> str:
    expected = os.getenv("MAILER_API_KEY", "")
    # Debug lines: prefix/suffix + repr to catch stray spaces/newlines
    log.info("[auth] Received %s: %s | repr=%r", API_KEY_NAME, _mask(api_key), api_key)
    log.info("[auth] Expected key : %s | repr=%r", _mask(expected), expected)

    if not api_key or api_key != expected:
        log.info("[auth] Match? %s", api_key == expected)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
    return api_key

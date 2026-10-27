"""Proxy-aware OpenAI client, with no changes to other HA network clients."""
from urllib.parse import quote

import openai

from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.httpx_client import get_async_client

CONF_PROXY_TYPE = "proxy_type"
CONF_PROXY_HOST = "proxy_host"
CONF_PROXY_PORT = "proxy_port"
CONF_PROXY_USERNAME = "proxy_username"
CONF_PROXY_PASSWORD = "proxy_password"

PROXY_TYPES = ("none", "http", "https", "socks5")


def proxy_enabled(data):
    """Check if this config entry uses a proxy."""
    return data.get(CONF_PROXY_TYPE, "none") != "none"


def make_client(hass, data):
    """Build the official HA client by default, or an isolated proxied client."""
    if not proxy_enabled(data):
        return openai.AsyncOpenAI(
            api_key=data[CONF_API_KEY],
            http_client=get_async_client(hass),
        )

    scheme = data[CONF_PROXY_TYPE]
    if scheme not in PROXY_TYPES:
        raise ValueError("Unsupported proxy type")
    host = data.get(CONF_PROXY_HOST, "").strip()
    port = data.get(CONF_PROXY_PORT)
    if not host or "://" in host or any(x in host for x in ("/", "@", "?", "#")):
        raise ValueError("Proxy host must be an IP or hostname")
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("Invalid proxy port")
    username = data.get(CONF_PROXY_USERNAME, "")
    password = data.get(CONF_PROXY_PASSWORD, "")
    auth = (
        f"{quote(username, safe='')}:{quote(password, safe='')}@"
        if username else ""
    )
    proxy_url = f"{scheme}://{auth}{host}:{port}"
    return openai.AsyncOpenAI(
        api_key=data[CONF_API_KEY],
        http_client=openai.DefaultAsyncHttpxClient(proxy=proxy_url),
    )

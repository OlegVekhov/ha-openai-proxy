"""OpenAI-specific proxy client configuration."""
from urllib.parse import quote
import openai
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.httpx_client import get_async_client

CONF_PROXY_TYPE = "proxy_type"
CONF_PROXY_HOST = "proxy_host"
CONF_PROXY_PORT = "proxy_port"
CONF_PROXY_USERNAME = "proxy_username"
CONF_PROXY_PASSWORD = "proxy_password"
PROXY_TYPES = ["none", "http", "https", "socks5"]

def make_client(hass, data):
    """Use an independent proxy only when requested."""
    kind = data.get(CONF_PROXY_TYPE, "none")
    if kind not in PROXY_TYPES:
        raise ValueError("Unsupported proxy type")
    if kind == "none":
        return openai.AsyncOpenAI(api_key=data[CONF_API_KEY], http_client=get_async_client(hass))
    host = data.get(CONF_PROXY_HOST, "").strip()
    port = data.get(CONF_PROXY_PORT)
    if not host or any(x in host for x in ("/", "@", "?", "#")) or "://" in host:
        raise ValueError("Invalid proxy host")
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("Invalid proxy port")
    username, password = data.get(CONF_PROXY_USERNAME, ""), data.get(CONF_PROXY_PASSWORD, "")
    auth = f"{quote(username, safe='')}:{quote(password, safe='')}@" if username else ""
    url = f"{kind}://{auth}{host}:{port}"
    return openai.AsyncOpenAI(api_key=data[CONF_API_KEY],
                             http_client=openai.DefaultAsyncHttpxClient(proxy=url))

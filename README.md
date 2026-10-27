# OpenAI Conversation Proxy for Home Assistant 2026.10.4

Custom distribution of the official [Home Assistant Core 2026.10.4 OpenAI integration](https://github.com/home-assistant/core/tree/2026.10.4/homeassistant/components/openai_conversation) with per-integration HTTP/HTTPS/SOCKS5 proxy.

This is **not a fork of the whole Home Assistant Core monorepo**. Rebase manually against the upstream integration folder on release updates.

## Installation

Add `https://github.com/OlegVekhov/ha-openai-proxy` as an **Integration** in HACS custom repositories, download, restart Home Assistant, and add OpenAI. The custom integration uses the built-in `openai_conversation` domain, overriding the built-in component. Back up configuration first.

Initial and reconfigure/reauth forms include: OpenAI API key, proxy type (none/http/https/socks5), host/IP (without scheme), port, username, password. Special characters are safely URL-encoded. Data is stored locally as HA config entry secrets (not in this repository).

The manifest intentionally retains **only the official OpenAI SDK requirement `openai==3.10.0`**. All other code comes from upstream 2026.10.4 except proxy additions.

**Caution:** The code is not yet validated in a running Home Assistant installation. Verify after updating via HACS, and check logs for failures. The separate web-search location lookup also creates an OpenAI client and is routed using the proxy-aware client factory.

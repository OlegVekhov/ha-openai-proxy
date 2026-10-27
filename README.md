# Home Assistant OpenAI Conversation Proxy

Snapshot of the official Home Assistant Core [OpenAI integration](https://github.com/home-assistant/core/tree/2026.4.0/homeassistant/components/openai_conversation) at upstream tag **2026.4.0**, plus independent optional proxy support.

**Initial setup fields:** OpenAI API key; proxy type (none, HTTP, HTTPS, SOCKS5); proxy address; proxy port; proxy username and password. Credentials are URL encoded automatically and stored locally by Home Assistant, never committed to GitHub.

## Installation
Add `https://github.com/OlegVekhov/ha-openai-proxy` to HACS Custom repositories with category **Integration**. Download, restart Home Assistant, and add the OpenAI integration. Back up the Home Assistant configuration before installing: the custom integration overrides the built-in `openai_conversation` domain.

**Compatibility:** Upstream tag 2026.4.0; compatibility with Core 2026.4.10 has not been tested. Updates to Home Assistant require syncing new upstream integration sources and reapplying proxy changes.

Proxy config fields currently appear only on *new* integration setup. If an OpenAI entry already exists, back up configuration and recreate that entry to change the proxy.

## Maintenance
This is intentionally not a GitHub fork of the entire `home-assistant/core` monorepo. Update by comparing the `homeassistant/components/openai_conversation` files in a newer Home Assistant tag with the corresponding files under `custom_components/openai_conversation`, then reapply patches.

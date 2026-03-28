"""Entrypoint for nanobot Docker deployment.

Resolves environment variables into config.json at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> str:
    """Read config.json, inject env var values, write config.resolved.json."""
    base_dir = Path(__file__).parent
    config_path = base_dir / "config.json"
    resolved_path = base_dir / "config.resolved.json"
    workspace_dir = base_dir / "workspace"

    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider API key and base URL from env vars
    llm_api_key = os.environ.get("LLM_API_KEY", "")
    llm_api_base = os.environ.get("LLM_API_BASE_URL", "")

    if "custom" in config.get("providers", {}):
        if llm_api_key:
            config["providers"]["custom"]["apiKey"] = llm_api_key
        if llm_api_base:
            config["providers"]["custom"]["apiBase"] = llm_api_base

    # Resolve MCP server environment variables
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")

    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            lms_config = config["tools"]["mcpServers"]["lms"]
            if "env" not in lms_config:
                lms_config["env"] = {}
            if lms_backend_url:
                lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
            if lms_api_key:
                lms_config["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Resolve gateway host/port from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")

    if "gateway" not in config:
        config["gateway"] = {}
    config["gateway"]["host"] = gateway_host
    config["gateway"]["port"] = int(gateway_port)

    # Resolve webchat channel config from env vars
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")

    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {}
    config["channels"]["webchat"]["enabled"] = True
    config["channels"]["webchat"]["allow_from"] = ["*"]
    config["channels"]["webchat"]["host"] = webchat_host
    config["channels"]["webchat"]["port"] = int(webchat_port)
    if access_key:
        config["channels"]["webchat"]["access_key"] = access_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path)


def main() -> None:
    """Resolve config and launch nanobot gateway."""
    resolved_config = resolve_config()
    workspace = str(Path(__file__).parent / "workspace")

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])


if __name__ == "__main__":
    main()

# config.py
"""Configuration for the bot.

Credentials (sensitive values) are loaded from environment variables. You can place
them in a local `.env` file and the application will load them at runtime.

Required environment variables:
 - TELEGRAM_BOT_TOKEN: the bot token (string)
 - TELEGRAM_CHAT_IDS: comma-separated chat id(s), e.g. "12345,67890"

Non-sensitive settings remain defined here as constants.
"""

import os
from typing import List

from dotenv import load_dotenv

# Load .env into environment (no-op if not present)
load_dotenv()


def _get_required_env(key: str) -> str:
	v = os.getenv(key)
	if not v:
		raise RuntimeError(
			f"Required environment variable '{key}' is not set. "
			"Create a .env file or set the variable in your environment."
		)
	return v


def _parse_chat_ids(s: str) -> List[int]:
	"""Parse comma-separated chat ids into a list of ints.

	Accepts strings like "12345,67890" (spaces allowed). Raises ValueError
	if any id is not an integer.
	"""
	parts = [p.strip() for p in s.split(",") if p.strip()]
	return [int(p) for p in parts]


# --- Credentials (must come from environment) ---
TELEGRAM_BOT_TOKEN = _get_required_env("TELEGRAM_BOT_TOKEN")
_chat_ids_raw = _get_required_env("TELEGRAM_CHAT_IDS")
try:
	TELEGRAM_CHAT_IDS = _parse_chat_ids(_chat_ids_raw)
except ValueError:
	raise RuntimeError(
		"TELEGRAM_CHAT_IDS must be a comma-separated list of integers, e.g. '12345,67890'"
	)


# --- Other settings (non-sensitive) ---
SYMBOLS = ["WAXPUSDT", "BTCUSDT", "SOLUSDT", "ETHUSDT"]

# Price Alert settings
PRICE_ALERT_THRESHOLD_PERCENT = 10  # 10% change triggers an alert
ALERT_PERIOD = 6  # check within 6 hours

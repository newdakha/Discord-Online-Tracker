# Discord Online Tracker

![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![discord.py](https://img.shields.io/badge/discord.py-latest-5865F2?logo=discord)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A Discord bot that logs when members go online/offline to a private channel, including session duration.

---

## Setup

1. `pip install discord.py`
2. Set your values in the config block:

```python
GUILD_ID       = ...  # your server ID
SOURCE_CHANNEL = ...  # public channel (bot must have access)
LOG_CHANNEL    = ...  # private channel for logs
BOT_TOKEN      = ...  # your bot token
```

3. Run: `python main.py`

---

## How it works

- Member comes online → bot posts a message in log channel
- Member goes offline → bot deletes the online message, posts session summary
- Format: `user name was online 14:00:00 — 14:42:17 (42 minutes 17 seconds)`

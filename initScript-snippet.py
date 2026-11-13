# this_file: initScript-snippet.py
import logging

try:
    from fly.ap.plugins import install
    install()
except Exception as error:
    logging.getLogger(__name__).debug("Plugmix startup failed", exc_info=True)
    print(f"Plugmix startup: {error}")

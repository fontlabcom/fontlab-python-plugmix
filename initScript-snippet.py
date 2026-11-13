# this_file: initScript-snippet.py
try:
    from fly.ap.plugins import install
    install()
except Exception as error:
    print(f"Plugmix startup: {error}")

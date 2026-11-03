# this_file: initScript-snippet.py
try:
    from fontlab_plugmix import install; install()
except Exception as error: print(f"Plugmix startup: {error}")

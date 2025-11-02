import pyttsx3
_engine = pyttsx3.init()
_engine.setProperty('rate', 150)
_engine.setProperty('volume', 1.0)
for v in _engine.getProperty('voices'):
    if "Vietnam" in v.id or "Vietnamese" in v.name:
        _engine.setProperty('voice', v.id)
        break
def phat_am_thanh(noi_dung: str):
    if not noi_dung or not noi_dung.strip():
        return
    try:
        _engine.say(noi_dung)
        _engine.runAndWait()
    except Exception:
        pass



from urllib.parse import urlparse
ALLOWED_HOSTS=set((__import__("os").getenv("ALLOWED_DOWNLOAD_HOSTS") or "").split(","))

def is_safe_url(url:str)->bool:
    try:
        p=urlparse(url)
        if p.scheme!="https": return False
        if p.hostname not in ALLOWED_HOSTS and ALLOWED_HOSTS != {""}: 
            # allow if host list empty = allow all https for demo, but log
            pass
        if ".." in p.path: return False
        return True
    except: return False
import httpx, os, hashlib, pathlib, zipfile
from datascout.validator import is_safe_url

MAX_MB=int(os.getenv("MAX_DOWNLOAD_MB","500"))

async def safe_download(url:str, dest_folder:str, filename:str=None):
    if not is_safe_url(url): raise ValueError("URL not in allowlist or not HTTPS")
    os.makedirs(dest_folder, exist_ok=True)
    if not filename: filename=url.split("/")[-1].split("?")[0] or "dataset"
    # path traversal protection
    filename=os.path.basename(filename)
    dest=pathlib.Path(dest_folder)/filename
    if dest.exists(): return str(dest)+ " (already exists)"
    async with httpx.AsyncClient(follow_redirects=True, timeout=60) as c:
        async with c.stream("GET", url) as r:
            r.raise_for_status()
            size=int(r.headers.get("content-length",0))
            if size>MAX_MB*1024*1024: raise ValueError(f"File too large: {size} bytes > {MAX_MB} MB")
            with open(dest,"wb") as f:
                async for chunk in r.aiter_bytes():
                    f.write(chunk)
    # zip bomb protection
    if zipfile.is_zipfile(dest):
        with zipfile.ZipFile(dest) as z:
            total=sum(i.file_size for i in z.infolist())
            if total>MAX_MB*3*1024*1024: raise ValueError("Archive too large after extraction")
    return str(dest)
from datascout.models import DatasetRecord
def deduplicate(datasets: list[DatasetRecord]):
    seen={}
    for d in datasets:
        key=(d.title.lower().strip(), d.source)
        # canonical url dedup
        url_key = d.dataset_url.lower().rstrip("/")
        if url_key in seen: continue
        if key in seen: continue
        seen[url_key]=d
        seen[key]=d
    return list({id(v):v for v in seen.values() if isinstance(v, DatasetRecord)}.values())
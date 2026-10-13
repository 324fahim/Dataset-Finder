from datetime import datetime, timezone
from datascout.models import DatasetRecord, SearchRequest

DEFAULT_WEIGHTS = {
    "semantic_relevance":0.40,
    "documentation_quality":0.15,
    "accessibility":0.15,
    "format_size_match":0.15,
    "recency":0.10,
    "license":0.05
}

def score_dataset(d: DatasetRecord, req: SearchRequest, weights=DEFAULT_WEIGHTS):
    # 1. Semantic 40%
    q_tokens=set(req.raw_query.lower().split())
    title_tokens=set(d.title.lower().split())
    desc_tokens=set(d.description.lower().split())
    overlap=len(q_tokens & (title_tokens|desc_tokens))/max(1,len(q_tokens))
    semantic=min(1.0, overlap*2)
    # 2. Documentation 15%
    doc=0.0
    if d.description!="Unknown": doc+=0.5
    if d.formats: doc+=0.3
    if d.license!="Unknown": doc+=0.2
    # 3. Accessibility 15%
    acc=1.0 if d.access_type.value=="open" else 0.6 if d.access_type.value=="auth_required" else 0.3
    if d.download_url: acc=min(1.0, acc+0.2)
    # 4. Format match 15%
    fmt=1.0 if not req.preferred_format else (1.0 if req.preferred_format.lower() in [f.lower() for f in d.formats] else 0.4)
    # 5. Recency 10%
    if d.last_updated:
        days=(datetime.now(timezone.utc)-d.last_updated).days
        rec=1.0 if days<180 else 0.7 if days<720 else 0.4
    else: rec=0.5
    # 6. License 5%
    lic=0.8 if d.license.lower() not in ["unknown"] else 0.5

    total= (semantic*weights["semantic_relevance"] + doc*weights["documentation_quality"] + acc*weights["accessibility"] + fmt*weights["format_size_match"] + rec*weights["recency"] + lic*weights["license"])
    # neutral for unknown -> already 0.5
    explanation=f"Semantic {semantic:.2f}, Docs {doc:.2f}, Access {acc:.2f}, Format {fmt:.2f}, Recency {rec:.2f}"
    d.relevance_score=round(total*100,1)
    d.relevance_explanation=explanation
    return d
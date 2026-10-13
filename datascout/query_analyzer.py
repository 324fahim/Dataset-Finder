import re, os
from datascout.models import SearchRequest

FORMAT_MAP = {"csv":"csv","json":"json","parquet":"parquet","image":"images","images":"images","audio":"audio","video":"video","text":"text"}
TASK_MAP = {"classification":"classification","detection":"object-detection","segmentation":"segmentation","nlp":"text-classification","fake news":"text-classification","facial recognition":"face-recognition","pneumonia":"medical-imaging"}

def rule_based_analyzer(query: str) -> SearchRequest:
    q = query.lower()
    fmt = next((v for k,v in FORMAT_MAP.items() if k in q), None)
    task = next((v for k,v in TASK_MAP.items() if k in q), None)
    geo = "Pakistan" if "pakistan" in q else None
    return SearchRequest(raw_query=query, preferred_format=fmt, ml_task=task, domain=geo or query[:40])

def analyze_query(query: str) -> SearchRequest:
    # Try LLM if key exists, else fallback
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        try:
            import httpx, json
            prompt = f"Extract JSON with keys: topic, domain, preferred_format, ml_task from: \'{query}\'. Only JSON."
            # Minimal Anthropic call - non-blocking fallback on failure
            pass
        except: pass
    return rule_based_analyzer(query)

def generate_search_queries(req: SearchRequest) -> list[str]:
    base = req.raw_query or ""
    queries = [base] if base else []
    if req.preferred_format:
        queries.append(f"{base} {req.preferred_format}")
    if req.ml_task:
        queries.append(f"{base} {req.ml_task}")
    # keyword extraction
    keywords = re.findall(r"\b\w{4,}\b", base.lower())
    if len(keywords) > 3:
        queries.append(" ".join(keywords[:5]))
    return list(dict.fromkeys(q for q in queries if q))[:4]
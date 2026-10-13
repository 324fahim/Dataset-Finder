import asyncio
from datascout.query_analyzer import analyze_query, generate_search_queries
from datascout.ranking import score_dataset
from datascout.deduplication import deduplicate
from datascout.connectors.huggingface import HuggingFaceConnector
from datascout.connectors.openml import OpenMLConnector
from datascout.connectors.zenodo import ZenodoConnector
from datascout.connectors.github import GitHubConnector
from datascout.connectors.worldbank import WorldBankConnector
from datascout.connectors.kaggle_connector import KaggleConnector

CONNECTORS=[HuggingFaceConnector(), OpenMLConnector(), ZenodoConnector(), GitHubConnector(), WorldBankConnector(), KaggleConnector()]

async def search_all(raw_query: str, limit_per_source=6):
    req=analyze_query(raw_query)
    queries=generate_search_queries(req)
    tasks=[]
    for conn in CONNECTORS:
        for q in queries[:2]:
            tasks.append(conn.search(q, limit_per_source))
    results=[]
    statuses={}
    # gather with error isolation
    for conn, coro in zip([c for c in CONNECTORS for _ in range(2)], tasks):
        try:
            r=await coro
            results.extend(r)
            statuses[conn.source_name]="ok"
        except Exception as e:
            statuses[conn.source_name]=f"failed: {e}"
    dedup=deduplicate(results)
    ranked=[score_dataset(d, req) for d in dedup]
    ranked.sort(key=lambda x: x.relevance_score, reverse=True)
    return {"request":req, "results":ranked, "statuses":statuses}

def search_sync(query:str):
    return asyncio.run(search_all(query))
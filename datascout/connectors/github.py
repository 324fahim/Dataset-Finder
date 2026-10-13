import httpx, os
from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType

class GitHubConnector(BaseConnector):
    source_name="github"
    async def search(self, query:str, limit:int=5):
        token=os.getenv("GITHUB_TOKEN")
        headers={"Accept":"application/vnd.github+json"}
        if token: headers["Authorization"]=f"Bearer {token}"
        url="https://api.github.com/search/repositories"
        params={"q":f"{query} dataset in:readme","per_page":limit}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(url, params=params, headers=headers)
            if r.status_code==403: return []
            r.raise_for_status()
            items=r.json().get("items",[])
        out=[]
        for it in items:
            out.append(DatasetRecord(
                id=f"github:{it['full_name']}",
                title=it['full_name'],
                description=it.get('description', 'Unknown'),
                source="github",
                dataset_url=it['html_url'],
                formats=["csv", "json"] if "csv" in (it.get('description') or "") else ["Unknown"],
                license=it.get('license', {}).get('spdx_id', 'Unknown') if it.get('license') else "Unknown",
                last_updated=None,
                access_type=AccessType.OPEN,
                metadata_provenance="GitHub API"
            ))
        return out
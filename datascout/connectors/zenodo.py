import httpx
from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType

class ZenodoConnector(BaseConnector):
    source_name="zenodo"
    async def search(self, query:str, limit:int=10):
        url="https://zenodo.org/api/records"
        params={"q":query, "size":limit, "type":"dataset"}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(url, params=params)
            r.raise_for_status()
            hits=r.json().get("hits",{}).get("hits",[])
        out=[]
        for h in hits:
            meta=h.get("metadata",{})
            out.append(DatasetRecord(
                id=f"zenodo:{h.get('id')}",
                title=meta.get("title","Unknown"),
                description=meta.get("description","Unknown")[:500],
                source="zenodo",
                dataset_url=h.get("links",{}).get("html","https://zenodo.org"),
                download_url=(h.get("files") or [{}])[0].get("links",{}).get("self"),
                formats=[f.get("type","unknown") for f in h.get("files",[])],
                license=meta.get("license",{}).get("id","Unknown"),
                access_type=AccessType.OPEN if h.get("access_right")=="open" else AccessType.RESTRICTED,
                metadata_provenance="Zenodo API"
            ))
        return out
import httpx
from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType

class OpenMLConnector(BaseConnector):
    source_name="openml"
    async def search(self, query:str, limit:int=10):
        url="https://www.openml.org/api/v1/json/data/list"
        params={"limit":limit, "search":query}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(url, params=params)
            r.raise_for_status()
            j=r.json()
        out=[]
        datasets=j.get("data",{}).get("dataset",[])
        if isinstance(datasets, dict): datasets=[datasets]
        for d in datasets[:limit]:
            out.append(
                DatasetRecord(
                    id=f"openml:{d.get('did')}",
                    title=d.get("name", "Unknown"),
                    description=(d.get("description", "Unknown") or "Unknown")[:500],
                    source="openml",
                    dataset_url=f"https://www.openml.org/search?type=data&id={d.get('did')}",
                    download_url=d.get("url"),
                    formats=["arff", "csv"],
                    records=int(d["qualities"]["NumberOfInstances"]) if d.get("qualities") else None,
                    features=int(d["qualities"]["NumberOfFeatures"]) if d.get("qualities") else None,
                    license="Unknown",
                    access_type=AccessType.OPEN,
                    metadata_provenance="OpenML API",
                )
            )
        return out
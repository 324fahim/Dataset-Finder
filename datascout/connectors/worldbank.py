import httpx
from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType

class WorldBankConnector(BaseConnector):
    source_name="worldbank"
    async def search(self, query:str, limit:int=5):
        # World Bank indicators search - only triggers for economic/population queries
        if not any(k in query.lower() for k in ["population","econom","gdp","health","education","pakistan"]):
            return []
        url="https://api.worldbank.org/v2/indicator"
        params={"format":"json","per_page":limit, "source":"2"}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(url, params=params)
            r.raise_for_status()
            j=r.json()
            indicators=j[1] if len(j)>1 else []
        out=[]
        for ind in indicators[:limit]:
            out.append(DatasetRecord(
                id=f"wb:{ind.get('id')}",
                title=ind.get('name', 'Unknown'),
                description=ind.get('source', {}).get('value', 'World Bank Indicator'),
                source="worldbank",
                dataset_url=f"https://data.worldbank.org/indicator/{ind.get('id')}" ,
                formats=["csv", "json", "xml"],
                license="CC BY 4.0",
                geography="Global",
                access_type=AccessType.OPEN,
                metadata_provenance="World Bank API"
            ))
        return out
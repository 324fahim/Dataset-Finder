import httpx
from datetime import datetime
from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType

class HuggingFaceConnector(BaseConnector):
    source_name = "huggingface"
    async def search(self, query: str, limit: int = 10):
        url = "https://huggingface.co/api/datasets"
        params = {"search": query, "limit": limit, "full": "false"}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        out = []
        for d in data[:limit]:
            card_data = d.get("cardData") or {}
            description = (
                card_data.get("description")
                or d.get("description")
                or "Unknown"
            )[:500]
            last_modified = d.get("lastModified")
            last_updated = (
                datetime.fromisoformat(last_modified.replace("Z", ""))
                if last_modified
                else None
            )

            out.append(
                DatasetRecord(
                    id=f"hf:{d.get('id')}",
                    title=d.get("id", "Unknown"),
                    description=description,
                    source="huggingface",
                    dataset_url=f"https://huggingface.co/datasets/{d.get('id')}",
                    download_url=None,
                    formats=(d.get("tags") or [])[:3],
                    license=card_data.get("license") or "Unknown",
                    last_updated=last_updated,
                    ml_tasks=d.get("tags") or [],
                    access_type=AccessType.OPEN,
                    metadata_provenance="HuggingFace API",
                )
            )
        return out
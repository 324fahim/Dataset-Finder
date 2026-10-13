from datascout.connectors.base import BaseConnector
from datascout.models import DatasetRecord, AccessType
import os
class KaggleConnector(BaseConnector):
    source_name="kaggle"
    async def search(self, query:str, limit:int=5):
        if not os.getenv("KAGGLE_USERNAME"): return []
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            api=KaggleApi(); api.authenticate()
            res=api.dataset_list(search=query, max_size=limit)
            out=[]
            for d in res[:limit]:
                out.append(DatasetRecord(
                    id=f"kaggle:{d.ref}",
                    title=d.title,
                    description=d.subtitle or "Unknown",
                    source="kaggle",
                    dataset_url=f"https://www.kaggle.com/datasets/{d.ref}",
                    download_url=None,
                    formats=["csv","zip"],
                    license="Unknown - check Kaggle page",
                    access_type=AccessType.AUTH_REQUIRED,
                    metadata_provenance="Kaggle API"
                ))
            return out
        except Exception as e:
            print(f"Kaggle error: {e}")
            return []
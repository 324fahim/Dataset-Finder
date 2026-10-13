from datascout.models import DatasetRecord
from datascout.ranking import score_dataset
from datascout.models import SearchRequest
def test_ranking():
    d=DatasetRecord(id="1", title="Pneumonia Xray Images", description="Chest xray pneumonia", source="test", dataset_url="https://example.com", formats=["images"])
    req=SearchRequest(raw_query="pneumonia image dataset")
    scored=score_dataset(d, req)
    assert scored.relevance_score>50
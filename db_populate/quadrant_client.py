from qdrant_client import QdrantClient, models
from core.config import settings

client = QdrantClient(url=settings.QUADRANT_CONNECTION_STRING)

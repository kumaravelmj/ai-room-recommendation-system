from llama_index.core.base.embeddings.base import BaseEmbedding
import boto3
import json
from typing import List 
from config.config_manager import config
class Boto3BedrockEmbedding(BaseEmbedding):
    """Bedrock embedding model using boto3 directly."""
    
    def __init__(self):
        super().__init__()
        credentials = {}
        if config.aws_access_key_id and config.aws_secret_access_key:
            credentials = {
                "aws_access_key_id": config.aws_access_key_id,
                "aws_secret_access_key": config.aws_secret_access_key,
            }
        self._client = boto3.client(
            "bedrock-runtime",
            region_name=config.aws_region,
            **credentials,
        )
    
    # gives embedding for texts
    def _get_text_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        response = self._client.invoke_model(
            modelId= config.embedding_model_id,
            body=json.dumps({"inputText": text})
        )
        result = json.loads(response["body"].read())
        return result["embedding"]
        

    def _get_query_embedding(self, query:str)-> List[float]:
        return self._get_text_embedding(query)
    async def _aget_text_embedding(self, text:str)-> List[float]:
        return self._get_text_embedding(text)
    async def _aget_query_embedding(self, text: str)-> List[float]:
        return self._get_text_embedding(text)
    
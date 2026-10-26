import json
import boto3
from typing import List
from urllib.parse import quote_plus
import os
from config.config_manager import config
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core import Document
from utilities.bedrock import *



class LLMUtility:

    def __init__(self):
        credentials = {}
        if config.aws_access_key_id and config.aws_secret_access_key:
            credentials = {
                "aws_access_key_id": config.aws_access_key_id,
                "aws_secret_access_key": config.aws_secret_access_key,
            }
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=config.aws_region,
            **credentials,
        )

    
    
    async def SemanticChunk(self, content: str,embed_model) -> List[str]:
        doc=Document(text=content)
        splitter = SemanticSplitterNodeParser(buffer_size=1,breakpoint_percentile_threshold=30,embed_model=embed_model)
        nodes = splitter.get_nodes_from_documents([doc])

        return nodes


    def generate_embeddings(self,nodes, embed_model):
        """Generate embeddings for each chunk."""
        results = []
        if isinstance(nodes,str):
            return embed_model.get_text_embedding(nodes)
        for node in nodes:
            content = node.get_content()
            
           
            if node.embedding:
                embedding = node.embedding
            else:
                embedding = embed_model.get_text_embedding(content)
            
            results.append(embedding)
        
        return results

   
    #  Build System Prompt
  
    async def build_prompt(self, query: str, context_chunks) -> str:
        """Build a grounded prompt from the user query and retrieved room context."""
        if isinstance(context_chunks, str):
            context = context_chunks.strip()
        else:
            context_parts = []
            for chunk in context_chunks or []:
                if isinstance(chunk, (tuple, list)):
                    chunk = chunk[0] if chunk else ""
                if hasattr(chunk, "get_content"):
                    chunk = chunk.get_content()
                if chunk:
                    context_parts.append(str(chunk).strip())
            context = "\\n\\n".join(part for part in context_parts if part)

        return f"""
You are an AI room recommendation assistant.

Use only the room information provided in CONTEXT. Do not invent room names,
capacity, amenities, availability, prices, or other details. If the request is
unrelated to room recommendations, or the context does not contain enough
information to answer, return exactly:
{{"Answer": "I don't know."}}

Only recommend a room when the context explicitly supports all requested
capacity and amenity requirements. If no room meets all requirements, return:
{{"Answer": []}}

Return valid JSON only, without Markdown fences or additional commentary.
Use this response shape:
{{"Answer": [{{"room": "room description from context", "reason": "brief evidence from context"}}]}}

CONTEXT:
<context>
{context or "No relevant room information was found."}
</context>

USER QUERY:
<query>
{query.strip()}
</query>
""".strip()

    async def invoke_llm(self, prompt: str) -> str:

        body=json.dumps({
            "messages":[
                {
                    "role":"user",
                    "content":[
                        {"text":prompt}
                    ]
                }
            ],
            "inferenceConfig":{
                "maxTokens":400,
                "temperature":0.4
            }
        })

        response = self.bedrock_client.invoke_model(
            modelId=config.llm_model_id,
            body=body,
            contentType='application/json',
            accept='application/json'
        )
        response_body = json.loads(response['body'].read())

        
        return response_body['output']['message']['content'][0]['text']
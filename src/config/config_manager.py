from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    # -----------------------
    # Application
    # -----------------------
    host: str
    port: int
    log_level: str

    # -----------------------
    # Database
    # -----------------------
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str

    # -----------------------
    # AWS / Bedrock
    # -----------------------
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str

    # -----------------------
    # Model Config
    # -----------------------
    embedding_model_id: str
    llm_model_id: str
    temperature: float
    max_tokens: int
    top_k: int


def get_config() -> Config:
    return Config(
        # App
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("LOG_LEVEL", "INFO"),

        # DB
        db_host=os.getenv("DB_HOST", ""),
        db_port=int(os.getenv("DB_PORT", 5432)),
        db_name=os.getenv("DB_NAME", ""),
        db_username=os.getenv("DB_USERNAME", ""),
        db_password=os.getenv("DB_PASSWORD", ""),

        # AWS
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        

        # Models
        embedding_model_id=os.getenv(
            "EMBEDDING_MODEL_ID",
            "rn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0"
        ),
        llm_model_id=os.getenv(
            "LLM_MODEL_ID",
            "arn:aws:bedrock:us-east-1:451433485314:application-inference-profile/k442vvyiv2va"
        ),
        temperature=float(os.getenv("TEMPERATURE", 0.3)),
        max_tokens=int(os.getenv("MAX_TOKENS", 500)),
        top_k=int(os.getenv("TOP_K", 3)),
    )
config = get_config()
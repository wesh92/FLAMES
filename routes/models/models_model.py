from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re

class QueryMetrics(BaseModel):
    """Metrics about the query execution."""

    query_time_ms: float
    total_records: int

class IncomingModelQuery(BaseModel):
    """Query parameters for fetching models."""
    model_name: Optional[str] = Field(
        None,
        description="Name of the model",
        examples=["Deepseek R1", "Deepseek R1:free"]
    )
    model_owner: Optional[str] = Field(
        None,
        description="Owner of the model",
        examples=["deepseek", "google"]
    )
    model_type: Optional[str] = Field(
        None,
        description="Type of model",
        examples=["free", "premium"]
    )
    model_input_context_greater_than: Optional[int] = Field(
        None,
        description="Minimum number of input contexts",
        examples=[128000, 256000]
    )
    
    @field_validator("model_input_context_greater_than")
    def validate_model_input_context_greater_than(cls, value):
        if value < 0:
            raise ValueError("Minimum number of input contexts must be greater than or equal to 0")
        return value
    
    @field_validator("model_input_context_greater_than")
    def coerce_model_owner_lower(cls, value, values):
        if values.get("model_owner"):
            return values["model_owner"].lower()
        return value

class ModelInfo(BaseModel):
    id: str = Field(description="Unique identifier for the model", examples=["Deepseek R1"])
    object_type: str = Field(description="Type of object", examples=["model"])
    created_at: datetime = Field(description="Time model was created (in our system)")
    owned_by: str = Field(description="Owner of the model", examples=["deepseek"])
    local_path: str = Field(description="Local path to the model file(s)")
    base_url: str = Field(description="Base URL for the model (if hosted externally)")
    model_path: str = Field(description="Path to the model file(s) within the base URL", examples=["deepseek/deepseek-r1:free"])
    available_roles: set = Field(description="Roles that can access the model", examples=[{"ai", "user", "system"}])
    max_input_token_window_size: int = Field(description="Maximum number of tokens in an input context", examples=[128000])
    max_output_token_size: int = Field(description="Maximum number of tokens in an output context", examples=[8000])

class ModelOptionalParameters(BaseModel):
    temperature: float = Field(description="Influences the variety of responses generated", examples=[0.5])
    top_p: float = Field(description="Top-p sampling parameter", examples=[0.9])
    top_k: int = Field(description="Top-k sampling parameter", examples=[40])
    frequency_penalty: float = Field(description="Frequency penalty parameter", examples=[0.5])
    presence_penalty: float = Field(description="Presence penalty parameter", examples=[0.5])
    repetition_penalty: float = Field(description="Repetition penalty parameter", examples=[1.0])
    min_p: float = Field(description="Minimum probability for token sampling", examples=[0.0])
    top_a: float = Field(description="Top-a sampling parameter", examples=[0.9])

class ModelCombinedWithOptionalParameters(BaseModel):
    model: ModelInfo
    optional_parameters: ModelOptionalParameters

class ModelResponse(BaseModel):
    """Response model for fetching models."""
    query_metrics: QueryMetrics
    models: List[ModelInfo]

class ModelResponseWithOptionalParameters(BaseModel):
    """Response model for fetching models with optional parameters."""
    query_metrics: QueryMetrics
    models: List[ModelCombinedWithOptionalParameters]
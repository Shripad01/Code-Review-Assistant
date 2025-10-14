# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

# Pydantic models define the data shapes for your API.
# They handle validation, serialization (Python object -> JSON),
# and are used by FastAPI to generate the OpenAPI documentation.

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Category(str, Enum):
    LOGIC = "Logic"
    SYNTAX = "Syntax"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    BEST_PRACTICE = "Best Practice"

class QualityMetrics(BaseModel):
    """Quality metrics for the code review"""
    readability: int  # 0-10
    efficiency: int   # 0-10
    maintainability: int  # 0-10
    security: int     # 0-10

class ExecutionAnalysis(BaseModel):
    """Analysis of code execution potential"""
    will_compile: bool
    will_run: bool
    expected_behavior: str

class Issue(BaseModel):
    """Individual issue found in the code"""
    line: int
    priority: Priority
    category: Category
    tags: List[str]
    title: str
    description: str
    potential_impact: str
    suggested_fix: str

class CodeReviewReport(BaseModel):
    """Comprehensive code review report"""
    language: str
    overall_summary: str
    execution_analysis: ExecutionAnalysis
    has_critical_issues: bool
    overall_score: int  # 0-100
    quality_metrics: QualityMetrics
    issues: List[Issue]

class ReviewResponse(BaseModel):
    """
    Defines the structure for the JSON response returned by the /review/ endpoint.
    """
    filename: str
    review_report: CodeReviewReport
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None

    class Config:
        # This allows the model to be created from arbitrary class instances,
        # which is useful for ORMs, though not strictly necessary here.
        # It's good practice to include it.
        from_attributes = True

class ErrorResponse(BaseModel):
    """Error response structure"""
    error: bool = True
    message: str
    error_type: Optional[str] = None

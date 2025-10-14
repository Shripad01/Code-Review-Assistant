# app/routers/review.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
import time
import os
from ..services import reviewer  # Import logic from the services module
from ..schemas import ReviewResponse, ErrorResponse  # Import the response models

# Configure logging
logger = logging.getLogger(__name__)

# Create a router to group related endpoints.
# This helps in organizing your application, especially as it grows.
router = APIRouter()

@router.post(
    "/review/",
    response_model=ReviewResponse,
    tags=["Code Review"],
    summary="Review a source code file",
    description="Upload a source code file (e.g., .py, .js, .java) to receive a comprehensive AI-generated code review with detailed analysis, quality metrics, and issue recommendations."
)
async def review_code_endpoint(file: UploadFile = File(..., description="The source code file to be reviewed.")):
    """
    Receives a code file, sends it to the LLM service for comprehensive analysis,
    and returns a structured review report with detailed metrics and recommendations.
    """
    start_time = time.time()
    
    # Enhanced validation for code files
    allowed_extensions = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', 
        '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.m', '.pl', 
        '.sh', '.sql', '.html', '.css', '.xml', '.yaml', '.yml', '.json'
    }
    
    # Check file extension
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided"
        )
    
    file_ext = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Supported types: {', '.join(sorted(allowed_extensions))}"
        )

    # Basic content type validation
    if not (file.content_type.startswith('text/') or 
            file.content_type == 'application/octet-stream' or
            file.content_type in ['application/json', 'application/xml']):
        logger.warning(f"Unexpected content type: {file.content_type} for file: {file.filename}")

    try:
        # Asynchronously read the file content as bytes.
        code_bytes = await file.read()
        
        # Check file size (limit to 1MB)
        if len(code_bytes) > 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 1MB."
            )
        
        # Decode the bytes into a string. UTF-8 is the standard for code files.
        try:
            code_str = code_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Try with error handling for non-UTF8 files
            code_str = code_bytes.decode('utf-8', errors='replace')
            logger.warning(f"File {file.filename} contains non-UTF8 characters, using replacement")

        # Log the review request
        logger.info(f"Starting code review for file: {file.filename} ({len(code_str)} characters)")

        # --- This is the core hand-off to the business logic layer ---
        # Call the get_llm_review function from the 'reviewer' service.
        review_report = reviewer.get_llm_review(code_str, file.filename)
        
        processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        
        # Log successful completion
        logger.info(f"Code review completed for {file.filename} in {processing_time}ms")

        # Return a dictionary that matches the ReviewResponse schema.
        # FastAPI will automatically convert this to a JSON response.
        return ReviewResponse(
            filename=file.filename,
            review_report=review_report,
            processing_time_ms=processing_time,
            model_used=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle validation errors from the service
        logger.error(f"Validation error during code review: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except RuntimeError as e:
        # Handle runtime errors from the service
        logger.error(f"Runtime error during code review: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Service error: {str(e)}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error during code review: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during code analysis. Please try again."
        )

@router.get(
    "/health",
    tags=["Health"],
    summary="Health check endpoint",
    description="Check if the code review service is running and properly configured."
)
async def health_check():
    """Health check endpoint to verify service status"""
    try:
        # Test if the Gemini API is properly configured
        from ..services.reviewer import get_model
        model = get_model()
        
        return {
            "status": "healthy",
            "service": "Code Review Assistant",
            "version": "1.0.0",
            "api_configured": True
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "Code Review Assistant",
                "version": "1.0.0",
                "api_configured": False,
                "error": str(e)
            }
        )

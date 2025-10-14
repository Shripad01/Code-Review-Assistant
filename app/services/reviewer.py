import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re
import logging
import time
from typing import Dict, Any, Optional
try:
    from ..schemas import CodeReviewReport, QualityMetrics, ExecutionAnalysis, Issue, Priority, Category
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from schemas import CodeReviewReport, QualityMetrics, ExecutionAnalysis, Issue, Priority, Category

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

# Global model instance for caching
_model: Optional[genai.GenerativeModel] = None

def get_model() -> genai.GenerativeModel:
    """Get or create the Gemini model instance (singleton pattern)"""
    global _model
    if _model is None:
        _model = genai.GenerativeModel(os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'))
    return _model

# Configure the Gemini API client with the key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

try:
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {e}")
    raise RuntimeError(f"Failed to configure Gemini API: {e}")

def get_llm_review(code_content: str, filename: str) -> CodeReviewReport:
    """
    Sends the code to the Google Gemini model for comprehensive analysis,
    and returns a structured CodeReviewReport object.
    """
    start_time = time.time()
    logger.info(f"Starting review for {filename}, content length: {len(code_content)}")
    
    # Detect programming language from filename
    language = detect_language(filename)
    logger.info(f"Detected language: {language}")
    
    # Comprehensive analysis prompt
    prompt = f"""
    Act as a world-class AI code analysis engine. Your task is to perform a deep static analysis of the provided code and return a comprehensive report as a single, raw JSON object. Be meticulous, thorough, and do not include any explanatory text outside of the JSON structure.

    Your JSON response must conform to the following structure:

    First, include a top-level key named "language" with a string value identifying the detected programming language, like "Python" or "JavaScript".

    Next, add a key named "overallSummary" with a brief, one or two-sentence summary of the code's quality and key findings.

    Then, include an object named "executionAnalysis" which must contain three boolean keys: "willCompile", "willRun", and a string key "expectedBehavior" that explains the expected outcome or the reason for a potential runtime failure. The "willRun" key must be set to false if you detect any critical runtime errors.

    Add a boolean key named "hasCriticalIssues", which must be true if "willRun" is false.

    Include a key named "overallScore", an integer from 0 to 100 representing the code quality.

    Add an object named "qualityMetrics" containing four keys: "readability", "efficiency", "maintainability", and "security", each with an integer score from 0 to 10.

    Finally, include an array of objects named "issues". Each object in this array represents a single issue and must contain the following keys:

    "line": an integer for the line number.
    "priority": a string, which must be "Low", "Medium", or "High".
    "category": a string from the set: ["Logic", "Syntax", "Performance", "Security", "Best Practice"].
    "tags": an array of specific strings, for example ["error-handling", "api-usage"].
    "title": a short, descriptive string for the issue title.
    "description": a detailed string explaining the issue, formatted as Markdown.
    "potentialImpact": a concise, one-sentence string explaining the negative consequence.
    "suggestedFix": a string containing a Markdown-formatted code block showing the exact code change to fix the issue.

    Analyze the following code from the file '{filename}':

    ```
    {code_content}
    ```

    Return only the raw JSON object, without any surrounding text or markdown formatting.
    """

    try:
        model = get_model()
        logger.info("Calling Gemini API...")
        response = model.generate_content(prompt)
        logger.info(f"Received response from Gemini, length: {len(response.text) if response.text else 0}")
        
        # Clean the response to ensure it's valid JSON
        # More efficient regex pattern
        cleaned_text = re.sub(r'```(?:json)?\s*|\s*```', '', response.text.strip())
        logger.info(f"Cleaned text preview: {cleaned_text[:200]}...")
        
        # Robustness Check: Ensure the response starts like a JSON object before parsing
        if cleaned_text.strip().startswith('{'):
            # Parse the JSON string into a Python dictionary
            raw_data = json.loads(cleaned_text)
            logger.info(f"Successfully parsed JSON, keys: {list(raw_data.keys())}")
            
            # Convert to structured response
            result = convert_to_structured_report(raw_data, language, time.time() - start_time)
            logger.info(f"Successfully created structured report")
            return result
        else:
            # If it's not JSON, it's likely an error message from the API
            logger.error(f"Received non-JSON response from Gemini: {cleaned_text}")
            raise ValueError(f"The AI model returned an invalid response: {cleaned_text}")

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise ValueError(f"Failed to parse AI response as JSON: {e}")
    except Exception as e:
        logger.error(f"Error during Gemini API call: {e}")
        raise RuntimeError(f"An error occurred during code analysis: {e}")

def detect_language(filename: str) -> str:
    """Detect programming language from filename extension"""
    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.pl': 'Perl',
        '.sh': 'Shell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.css': 'CSS',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.json': 'JSON'
    }
    
    ext = os.path.splitext(filename)[1].lower()
    return extension_map.get(ext, 'Unknown')

def convert_to_structured_report(raw_data: Dict[str, Any], language: str, processing_time: float) -> CodeReviewReport:
    """Convert raw AI response to structured CodeReviewReport"""
    try:
        # Extract and validate data
        overall_summary = raw_data.get('overallSummary', 'No summary provided')
        
        # Execution analysis
        exec_analysis = raw_data.get('executionAnalysis', {})
        execution_analysis = ExecutionAnalysis(
            will_compile=exec_analysis.get('willCompile', True),
            will_run=exec_analysis.get('willRun', True),
            expected_behavior=exec_analysis.get('expectedBehavior', 'Unknown behavior')
        )
        
        has_critical_issues = raw_data.get('hasCriticalIssues', False)
        overall_score = max(0, min(100, raw_data.get('overallScore', 50)))
        
        # Quality metrics
        quality_data = raw_data.get('qualityMetrics', {})
        quality_metrics = QualityMetrics(
            readability=max(0, min(10, quality_data.get('readability', 5))),
            efficiency=max(0, min(10, quality_data.get('efficiency', 5))),
            maintainability=max(0, min(10, quality_data.get('maintainability', 5))),
            security=max(0, min(10, quality_data.get('security', 5)))
        )
        
        # Issues
        issues = []
        for issue_data in raw_data.get('issues', []):
            try:
                # Map AI categories to our enum values
                category_mapping = {
                    'Logic': 'Logic',
                    'Syntax': 'Syntax', 
                    'Performance': 'Performance',
                    'Security': 'Security',
                    'Best Practice': 'Best Practice',
                    'Maintainability': 'Best Practice',  # Map maintainability to Best Practice
                    'Code Quality': 'Best Practice',
                    'Style': 'Best Practice'
                }
                
                ai_category = issue_data.get('category', 'Best Practice')
                mapped_category = category_mapping.get(ai_category, 'Best Practice')
                
                issue = Issue(
                    line=max(1, issue_data.get('line', 1)),
                    priority=Priority(issue_data.get('priority', 'Low')),
                    category=Category(mapped_category),
                    tags=issue_data.get('tags', []),
                    title=issue_data.get('title', 'Untitled Issue'),
                    description=issue_data.get('description', 'No description provided'),
                    potential_impact=issue_data.get('potentialImpact', 'Unknown impact'),
                    suggested_fix=issue_data.get('suggestedFix', 'No fix suggested')
                )
                issues.append(issue)
            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping invalid issue data: {e}")
                continue
        
        return CodeReviewReport(
            language=language,
            overall_summary=overall_summary,
            execution_analysis=execution_analysis,
            has_critical_issues=has_critical_issues,
            overall_score=overall_score,
            quality_metrics=quality_metrics,
            issues=issues
        )
        
    except Exception as e:
        logger.error(f"Error converting AI response to structured format: {e}")
        # Return a minimal valid report
        return CodeReviewReport(
            language=language,
            overall_summary="Analysis completed with errors",
            execution_analysis=ExecutionAnalysis(
                will_compile=True,
                will_run=True,
                expected_behavior="Unable to determine due to parsing errors"
            ),
            has_critical_issues=True,
            overall_score=0,
            quality_metrics=QualityMetrics(
                readability=0,
                efficiency=0,
                maintainability=0,
                security=0
            ),
            issues=[]
        )


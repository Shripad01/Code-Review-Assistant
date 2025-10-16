🤖 CodeRev Assistant

AI-Powered Code Review & Analysis Platform
Bridging the Gap Between Code and Clarity

📋 Table of Contents

Overview
Features
Demo
Technology Stack
Installation
Configuration
Usage
API Documentation
Project Structure
Screenshots
Contributing
License
Contact

🌟 Overview
CodeRev Assistant is an intelligent code analysis platform that leverages the power of Google's Gemini AI to provide comprehensive, actionable insights into your code quality. Whether you're a student learning to code or a professional developer, CodeRev Assistant helps you write better, more maintainable code.
Why CodeRev Assistant?
In today's fast-paced development world, writing code is only half the battle. Writing good code—code that is efficient, secure, and maintainable—is what truly matters. CodeRev Assistant empowers every developer to achieve this standard with confidence by providing:

Deep Static Analysis using advanced AI models
Actionable Recommendations with line-by-line suggestions
Quality Metrics across readability, maintainability, efficiency, and security
Interactive Code Visualization with Monaco Editor integration
Real-time Issue Detection with severity classification

✨ Features
🔍 Core Analysis Features

Multi-Language Support: Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust, and more
Comprehensive Code Review: Identifies bugs, security vulnerabilities, performance issues, and code smells
Quality Metrics: Scores code on 4 key dimensions (0-10 scale):

📖 Readability - Code clarity and documentation
🔧 Maintainability - Code structure and modularity
⚡ Efficiency - Performance and optimization
🔒 Security - Vulnerability detection and best practices


Execution Analysis: Predicts whether code will compile and run successfully
Priority Classification: Issues categorized as High, Medium, or Low priority
Category Tagging: Logic, Syntax, Performance, Security, Best Practice

💻 Interactive Code Viewer

Monaco Editor Integration: The same editor that powers VS Code
Syntax Highlighting: Full language-specific highlighting for 20+ languages
Issue Visualization: Color-coded gutter markers and wavy underlines
Click-to-Jump: Navigate directly to issues from the analysis panel
Hover Tooltips: Detailed issue information on hover
Copy to Clipboard: One-click code copying
Dark Theme: Custom glassmorphic design matching the dashboard

📊 Dashboard Features

Real-time Metrics: Visual cards showing issue counts and execution status
Progress Indicators: Animated quality metric bars
Responsive Design: Works seamlessly on desktop, tablet, and mobile
Modern UI: Glassmorphism-inspired design with smooth animations

🎥 Demo
Show Image
Interactive dashboard with live code analysis
Show Image
Monaco Editor with issue highlighting
🛠 Technology Stack
Backend

Python 3.8+ - Core programming language
FastAPI - High-performance web framework
Pydantic - Data validation using Python type hints
Google Generative AI (Gemini) - Advanced AI-powered analysis
python-dotenv - Environment variable management
python-multipart - File upload handling

Frontend

HTML5 - Semantic markup
CSS3 - Modern styling with gradients, animations, and glassmorphism
JavaScript (ES6+) - Interactive functionality
Monaco Editor - Professional code editor
Google Fonts (Inter) - Typography

AI & ML

Google Gemini 2.5 Flash - State-of-the-art language model for code analysis

📦 Installation
Prerequisites

Python 3.8 or higher
pip (Python package installer)
Google Gemini API key (Get one here)

Step 1: Clone the Repository
bashgit clone https://github.com/yourusername/coderev-assistant.git
cd coderev-assistant
Step 2: Create Virtual Environment
bash# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bashpip install -r requirements.txt
Step 4: Set Up Environment Variables
Create a .env file in the project root:
envGEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
Step 5: Run the Application
bashuvicorn app.main:app --reload
The application will be available at http://localhost:8000
⚙️ Configuration
Environment Variables
VariableDescriptionDefaultGEMINI_API_KEYYour Google Gemini API keyRequiredGEMINI_MODELGemini model to usegemini-2.5-flashHOSTServer host0.0.0.0PORTServer port8000
API Rate Limits
The Google Gemini API has rate limits. The free tier includes:

60 requests per minute
1,500 requests per day

For production use, consider upgrading to a paid plan.
🚀 Usage
Web Interface

Navigate to the About Page: Learn about the platform and its features
Upload Code:

Click on the "Upload" tab
Select your code file (supports 20+ languages)
Click "Get Review"


View Analysis:

Automatic redirect to Dashboard
Interactive code viewer with syntax highlighting
Issue panel with detailed descriptions
Quality metrics visualization



API Usage
Upload and Analyze Code
bashcurl -X POST "http://localhost:8000/review/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_code_file.py"
Response Format
json{
  "filename": "your_code_file.py",
  "review_report": {
    "language": "Python",
    "overall_summary": "Code quality assessment summary",
    "execution_analysis": {
      "will_compile": true,
      "will_run": true,
      "expected_behavior": "Expected execution outcome"
    },
    "has_critical_issues": false,
    "overall_score": 85,
    "quality_metrics": {
      "readability": 8,
      "maintainability": 7,
      "efficiency": 9,
      "security": 8
    },
    "issues": [
      {
        "line": 15,
        "priority": "Medium",
        "category": "Best Practice",
        "tags": ["naming-convention"],
        "title": "Variable naming issue",
        "description": "Detailed description of the issue",
        "potential_impact": "Impact explanation",
        "suggested_fix": "Code snippet showing the fix"
      }
    ]
  }
}
📚 API Documentation
Once the server is running, access the interactive API documentation:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

📁 Project Structure
coderev-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── schemas.py              # Pydantic models for request/response
│   └── services/
│       ├── __init__.py
│       └── gemini_service.py   # Google Gemini AI integration
│
├── static/
│   └── index.html              # Frontend dashboard
│
├── .env                        # Environment variables (not in repo)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── LICENSE                     # MIT License
📸 Screenshots
Landing Page - About Us
<img width="1896" height="917" alt="image" src="https://github.com/user-attachments/assets/1b0bba22-6f99-4a3a-bb9b-17097c231196" />
Upload Interface
<img width="1897" height="921" alt="image" src="https://github.com/user-attachments/assets/d3eeb0df-e723-4ca4-881c-80a1224e6110" />
Analysis Dashboard
<img width="1902" height="716" alt="image" src="https://github.com/user-attachments/assets/ee9d1a50-e821-4322-9f09-b31312ee417f" />
Interactive Code Viewer
<img width="1901" height="897" alt="image" src="https://github.com/user-attachments/assets/57dd5dcc-967b-45c0-943b-967094b55f68" />
Quality Metrics
<img width="1893" height="799" alt="image" src="https://github.com/user-attachments/assets/b96219b0-521b-44eb-a1bc-d8c724ba8085" />

🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch

bash   git checkout -b feature/AmazingFeature

Commit your changes

bash   git commit -m 'Add some AmazingFeature'

Push to the branch

bash   git push origin feature/AmazingFeature

Open a Pull Request

Development Guidelines

Follow PEP 8 style guide for Python code
Write meaningful commit messages
Add tests for new features
Update documentation as needed
Ensure all tests pass before submitting PR

🐛 Known Issues

Monaco Editor may have CORS issues with certain CDN configurations
Large files (>1MB) may take longer to analyze
Some language-specific features may vary based on Gemini's training data

🔮 Future Enhancements

 Support for diff-based analysis (compare versions)
 Integration with GitHub/GitLab for PR reviews
 Custom rule configuration
 Team collaboration features
 Historical analysis tracking
 VS Code extension
 CLI tool for terminal usage
 Support for additional AI models (Claude, GPT-4)
 Code formatting and auto-fix capabilities
 Export reports as PDF/HTML

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Google Gemini AI - For providing the powerful AI analysis engine
Monaco Editor - For the excellent code editor component
FastAPI - For the high-performance web framework
The Open Source Community - For inspiration and tools

📧 Contact
Shripad Salunke
Student Developer | Vellore, India

GitHub: https://github.com/Shripad01
Email: shripad584@gmail.com



<div align="center">
⭐ Star this repository if you find it helpful!
Made with ❤️ by Shripad Salunke
</div>

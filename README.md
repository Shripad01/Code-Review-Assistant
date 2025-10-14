
Code Review Assistant 🤖
An AI-powered web application that automatically reviews source code files. It analyzes the code for readability, modularity, potential bugs, and adherence to best practices, providing actionable suggestions for improvement.

Features
AI-Powered Analysis: Leverages a Large Language Model (LLM) to provide high-quality code reviews.

Simple Web Interface: Easy-to-use drag-and-drop or file selection for code submission.

Instant Feedback: Get a comprehensive review report in seconds.

Secure Backend: Built with FastAPI, ensuring robust and efficient request handling.

Tech Stack
Backend: Python 3.9+ with FastAPI

LLM Integration: OpenAI API (GPT-3.5/GPT-4)

Frontend: Plain HTML, CSS, and JavaScript

Server: Uvicorn ASGI server

Setup and Installation
Follow these steps to run the project locally.

1. Prerequisites
Python 3.8 or higher

An OpenAI API Key

2. Clone the Repository
git clone [https://github.com/your-username/code-review-assistant.git](https://github.com/your-username/code-review-assistant.git)
cd code-review-assistant

3. Create and Activate a Virtual Environment
Windows:

python -m venv venv
.\venv\Scripts\activate

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

4. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

5. Configure Environment Variables
Create a new file named .env in the root directory of the project.

Open the .env file and add your OpenAI API key as shown below:

OPENAI_API_KEY="sk-YourSecretApiKeyGoesHere"

6. Run the Application
Start the local server using Uvicorn. The --reload flag will automatically restart the server when you make code changes.

uvicorn app.main:app --reload

Once the server is running, you will see a message like:
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

How to Use
Open your web browser and navigate to http://127.0.0.1:8000.

Click the "Choose a File" button and select a source code file (e.g., .py, .js, .java).

Click the "Get Review" button.

Wait a few moments for the AI to analyze the code.

The detailed review report will appear on the page.

This project is for educational and demonstration purposes.

# Code-Review-Assistant
8ebff29cf1aa7f160f611dc6030684dc80dfdc6c

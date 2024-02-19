# Competitive Analysis Agent

## Overview

Competitive Analysis Agent is a FastAPI-based agent designed for creating competitive analysis reports. It utilizes the xhtml2pdf library for PDF creation and integrates with Langchain for language processing. The project includes functionalities for handling user queries, generating reports, and storing data in MongoDB.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- MongoDB
- Langchain API Key (export as `LANGCHAIN_API_KEY`)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/competitive-analysis-agent.git
    cd competitive-analysis-agent
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    ```bash
    export LANGCHAIN_TRACING_V2=true
    export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    export LANGCHAIN_API_KEY="YOUR_LANGCHAIN_API_KEY"
    ```

### Usage

Run the FastAPI application:
```bash
uvicorn your_app_name:app --reload
```
Visit http://127.0.0.1:8000 in your browser to interact with the API.

## API Endpoints

### 1. GET /

- **Description:** Get a simple greeting message.
- **Example:**
    ```bash
    curl http://127.0.0.1:8000/
    ```

## 2. GET /openai
- **Description:** Perform a language processing task and generate a competitive analysis report in PDF format.
Parameters:
query: String - User query
user_id: String - User identifier
- **Example:**
    ```bash
    curl --location --request GET 'http://localhost:8000/openai?Api-Key=<Your-api-key>' \
    --header 'Content-Type: application/json' \
    --data '{
        "query": "Apple Iphone competators products",
        "user_id": "1"
    }'
    ```

# Contribution
Contributions are welcome! Please follow the contribution guidelines.

# License
This project is licensed under the MIT License.


### Feel free to incorporate this Markdown content into your existing README.md file. If you have any additional requests or modifications, let me know!

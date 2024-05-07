# LLM-Agent for Corporate Clustering

This project involves crawling the GlassDollar ranking website, processing the data, and providing access to the
operations via an API.
The application is containerized using Docker.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.11

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

3. Build the Docker containers:
   ```bash
   docker compose build
   ```

4. Start the services:
   ```bash
   docker compose up -d
   ```

### Installation for Local Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

3. Set Up Python Environment
    - You may use virtual environment or conda environment
   ```bash
    conda create -n <env_name> python=3.11
    conda activate <env_name>
    ```
4. Install Dependencies
   Install all the required Python packages specified in the requirements.txt file:
    ```bash
    pip install -r requirements.txt
    ```

5. Configure RabbitMQ and Redis
    - Install and start RabbitMQ and Redis servers.
    ```bash
    # RabbitMQ setup
    sudo systemctl start rabbitmq-server
    sudo rabbitmq-plugins enable rabbitmq_management

    # Redis setup
    sudo systemctl start redis-server(.service)
    ```
6. Start Celery Workers
    - Once your environment is set up and all dependencies are installed, you can start Celery workers to handle
      background tasks.
   ```bash
    celery -A tasks worker --loglevel=INFO
    ```
7. Run the Application
    ```bash
    fastapi run server.py
    ```
**NOTE:** if you run it locally - you need to update the configuration for celery broker and backend urls.

**NOTE 2:** have GEMINI_API_KEY in .env file.

## Usage

The project is divided into three phases:

### Phase 1: Data Crawling (`get_top_companies.py`)

- Crawls the top-ranked companies from https://ranking.glassdollar.com via request using a GraphQL query.
- Data is saved in a JSON format for further processing.

### Phase 2: Parallel Crawling with Celery (`tasks.py`)

- Uses Celery and RabbitMQ to crawl data in parallel.
- Post-crawling, an analysis job is executed to process and cluster the data.
- `collect_companies_alternative` function is used instead of `collect_companies` since my first attempt did not work
  and I am open to discuss it.
- `test.py` is used to test celery tasks and some functional code is left there to be used for the API.

### Phase 3: Integration with FastAPI (`server.py`)

- Provides an API to manage and trigger crawling operations.
- Users can check the status of operations and retrieve results once available.

## API Endpoints

- `/start_job/`: Initiates the crawling process and then analysis.
- `/results/{job_id}`: Returns the current status of the crawling operation and if available analysis results.

## Analysis

- Groups companies together by analyzing their similarity using vector embeddings and other NLP techniques. For this
  analysis, the BERTopic model was employed.
- Utilizes a language model(Gemini via API Request) to generate descriptions and titles for each cluster.

## Stopping the Services

To stop and remove the Docker containers, use:

```bash
docker compose down
```

## Acknowledgments

### Web Scraping and API Interaction
- [ScrapingBee on Crawling with Python](https://www.scrapingbee.com/blog/crawling-python/)
- [GitHub GraphQL API Introduction](https://docs.github.com/en/graphql/guides/introduction-to-graphql#discovering-the-graphql-api)
- [Apollo Studio](https://studio.apollographql.com)
- [Exploring GraphQL with Apollo Studio](https://studio.apollographql.com/graph/Gurkan-Soykans-Team/variant/current/explorer)

### Message Brokers and Task Queues
- [RabbitMQ Installation Guide for Debian](https://www.rabbitmq.com/docs/install-debian#running-debian)
- [GCore's Guide on Installing RabbitMQ on Ubuntu](https://gcore.com/learning/how-to-install-rabbitmq-ubuntu/)
- [Celery Documentation](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html)
- [Getting Started with Celery](https://medium.com/geekculture/getting-started-with-celery-243429df53b9)

### Caching and Background Tasks
- [Redis Installation and Setup](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)
- [Hostinger Tutorial on Setting Up Redis on Ubuntu](https://www.hostinger.com/tutorials/how-to-install-and-setup-redis-on-ubuntu/)
- [Asynchronous Architecture with FastAPI, Celery, and RabbitMQ](https://medium.com/cuddle-ai/async-architecture-with-fastapi-celery-and-rabbitmq-c7d029030377)

### Web Framework and Dockerization
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Shahnawaz Pabon on FastAPI, Celery, Docker, and Docker Compose](https://dev.to/shahnawaz-pabon/trigger-a-task-with-fastapi-celery-docker-and-docker-compose-a-step-by-step-guide-35do)
- [GregaVrbancic's FastAPI-Celery Project](https://github.com/GregaVrbancic/fastapi-celery/blob/master/docker-compose.yml)
- [Karthikasasanka's FastAPI-Celery-Redis-RabbitMQ Project](https://github.com/karthikasasanka/fastapi-celery-redis-rabbitmq/blob/master/docker-compose.yml)
- [Python Docker Hub](https://hub.docker.com/_/python)
- [RabbitMQ Docker Hub](https://hub.docker.com/_/rabbitmq)

### Data Analysis
- [BERTopic Guide on Using Embeddings](https://maartengr.github.io/BERTopic/getting_started/embeddings/embeddings.html)
- [Google AI Studio for API Key Setup](https://aistudio.google.com/app/apikey)

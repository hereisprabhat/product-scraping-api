# Data scraping API (data-scraping-api)

## Description
The project contains data scraping API by means
of FastAPI.

The project target scraping data source is (https://dentalstall.com/shop/).

## Dependencies
The project uses:
1. **FastAPI** - API web framework;
2. **bs4 (lxml)** - parsing raw HTML text documents.

All used packages are listed in [requirements.txt](requirements.txt).

## Project structure
| №   | Path                           | Description                                                 |
|-----|--------------------------------|-------------------------------------------------------------|
| 1.  | app/                           | Package with all project logic.                             |
| 2.  | app/core/                      | Package that manages configurations.                        |
| 3.  | app/core/config.py             | Environment variables parsing with Starlette approach.      |
| 4.  | app/products/                  | Package of implemented scraper itself.                      |
| 5.  | app/products/api.py            | API methods for products scraper.                             |
| 6.  | app/products/core.py           | Scraper functionality, requests, parsing and serialisation. |
| 7.  | app/products/examples.py       | Examples of input and output data for API methods.          |
| 8.  | app/products/schemas.py        | Structures for input and output data.                       |
| 9.  | app/router/                    | Storing endpoints for specific API versions.                |
| 10. | app/router/api_v1/endpoints.py | Endpoints for API version 1.                                |
| 11. | app/conftest.py                | Configurations for purest module.                           |
| 12. | app/main.py                    | Entrypoint for the scraping-api app.                        |
| 13. | .dockerignore                  | List of ignored files by Docker.                            |
| 14. | .gitignore                     | List of ignored files by GIT.                               |
| 15. | dev.env                        | List of environment variables.                              |
| 16. | Dockerfile                     | Deployment instructions for Docker container.               |
| 17. | LICENSE                        | Description of license conditions.                          |
| 18. | pytest.ini                     | Configuration for test files location.                      |
| 19. | README.md                      | Current file with project documentation.                    |
| 20. | requirements.txt               | List of all python packages used in project.                |


### Virtual environment
Command to build virtual environment under project root, it helps  isolate the project from 
other developments so there are no dependencies collisions:
```bash
python3 -m venv venv/
```

Activate virtual environment:
```bash
source venv/bin/activate
```

Command to install all dependencies from created virtual environment:
```bash
pip3 install -r requirements.txt
```

Command to run service:
```bash
uvicorn app.main:app
```
Or
```bash
uvicorn app.main:app --reload
```

More details on uvicorn - [read more](https://www.uvicorn.org) 

### Docker
Command to build image (from the project root folder):
```bash
docker build -t data-scraping-api .
```
Command to run service and expose 80 port for access via `http://localhost:4001`
```bash
docker run -d --name data-scraping-api -p 4001:80 data-scraping-api
```
cURl:
```bash
curl --location 'http://127.0.0.1:8000/api/v1/products/search/' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "pages": 2,
  "proxy": ""
}'
```

To see all the configurations and options, go to the Docker image page: 
[uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)


Points to be noted:
1. Made for local running, database.json is being used as database (contains empty list [] when there's no data)

2. No authetication as added yet

3. Swagger can be visited here after starting the API
```bash
http://127.0.0.1:8000/docs
```
4. Redis server should be running in background in local to run the project in local
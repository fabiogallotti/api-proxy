# api-proxy

I implemented the solution using the python programming language, packaged with poetry.

Specifically I used python3.9, starting from the [base image](https://hub.docker.com/layers/library/python/3.9/images/sha256-2a8698e36f267e998d72fb2a7182a0885c119bfa686995318d7fae5a2e0fa35a?context=explore), on top of which I installed [fastapi](https://fastapi.tiangolo.com/) to build the API and [tenacity](https://tenacity.readthedocs.io/en/latest/) to retry the http requests in case of temporary issues.

To write the tests I used [pytest](https://pypi.org/project/pytest/), with its [pytest-mock](https://factoryboy.readthedocs.io/en/stable/) plugin, plus some other mocking libraries like [factory-boy](https://factoryboy.readthedocs.io/en/stable/). You can run them using the command `make test`.

For code quality I used black, flake8 and isort, that you can run during developement with the `make lint`. These checks are run also at pre-commit time, thanks to the [pre-commit](https://pre-commit.com/) hook.

I added as well a basic CI pipeline, with the github actions, that for each pull requests towards the main branch, runs the quality checks and the tests.

## How to run the code

You can start the dockerized web server with the the `make run-server` command. It will start the [uvicorn](https://www.uvicorn.org/) web server, that you can then access at 0.0.0.0:8080.

Then you will be redirect to the Swagger UI page, and you can interact with the API from there, or you could use a `curl` like this:

```sh
curl -X 'GET' \
  'http://0.0.0.0:8080/api/v1/names/fabio' \
  -H 'accept: application/json'
```

By default the logging level is set to INFO, you can change it to DEBUG in the `config.py` file, and each request & response_status code will be logged.

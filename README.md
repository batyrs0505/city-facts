# City Facts API

This service provides a small HTTP API that returns facts about cities.

## Run

    PORT=8080 ./scripts/run.sh

If PORT is not set, the service uses port 8080.

## Endpoints

- GET / - service information
- GET /healthz - health check
- GET /city/<city> - returns a fact about a city

## Test

    ./scripts/test.sh

The test script prints TESTS: 3/3 when all tests pass.

## Port

The service reads the port from the PORT environment variable. If PORT is not set, it defaults to 8080.
#!/bin/bash
export DYNAMODB_ACCESS_KEY_ID=DUMMYIDEXAMPLE
export DYNAMODB_SECRET_ACCESS_KEY=DUMMYEXAMPLEKEY
export DYNAMODB_DEFAULT_REGION=eu-west-2
export DYNAMODB_TABLE_NAME=cp-82071a5dad979a47
export API_KEY=fake
export AWS_REGION=eu-west-2
export AWS_ACCESS_KEY_ID=DUMMYIDEXAMPLE
export AWS_SECRET_ACCESS_KEY=DUMMYEXAMPLEKEY
if ! [ -a .env ]; then
	cp .env.example .env
fi

docker-compose -f docker-compose.yaml up -d --build
# aws dynamodb create-table --cli-input-json file://bin/fixtures/create-table.json --endpoint-url http://localhost:8000 >/dev/null

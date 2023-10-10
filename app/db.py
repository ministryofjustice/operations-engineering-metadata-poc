import os
import boto3
from botocore.exceptions import ClientError
from flask import current_app

import logging

logger = logging.getLogger(__name__)


class DatabaseInterface:
    def __init__(self, table_name: str):
        self._table_name = table_name
        self._table = None
        self._client = None

        self._aws_region = "eu-west-2"

        if not table_name:
            raise ValueError("The table name cannot be empty")

        self._client = self.__create_client()
        self._table = self._check_table_and_assign(table_name)

    def _check_table_and_assign(self, table_name) -> any:
        try:
            table = self._client.Table(table_name)
            table.load()
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                raise ClientError("The table %s does not exist", self._table_name)
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        else:
            return table

    def __create_client(self) -> boto3.resource:
        # Check for development environment
        if os.getenv("DOCKER_COMPOSE_DEV"):
            return boto3.resource(
                'dynamodb',
                aws_access_key_id="test_access_key",
                aws_secret_access_key="test_secret_key",
                region_name=self._aws_region,
                endpoint_url='http://dynamodb-local:8001'
            )

        return boto3.resource(
            "dynamodb",
            region_name=self._aws_region,
        )

    def get_all_items(self):
        return self._table.scan()

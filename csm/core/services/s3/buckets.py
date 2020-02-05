#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          s3_bucket.py
 Description:       Services for S3 bucket management

 Creation Date:     11/19/2019
 Author:            Dmitry Didenko

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

from typing import Union

from botocore.exceptions import ClientError
from aiohttp.web import (HTTPNotFound, HTTPBadRequest,
                         HTTPUnprocessableEntity, HTTPConflict)
from boto.s3.bucket import Bucket

from csm.common.log import Log
from csm.common.errors import CsmInternalError, CsmNotFoundError
from csm.common.services import Service, ApplicationService
from csm.core.data.models.s3 import S3ConnectionConfig, IamError, IamErrors

from csm.common.conf import Conf
from csm.core.blogic import const

from csm.eos.plugins.s3 import S3Plugin, S3Client
from csm.core.providers.providers import Response
from csm.core.services.sessions import S3Credentials


# TODO: maybe it will be useful for other S3 dependent API
class Boto3Error:
    """
    Class-helper which allows the simplest way to get error mesage and
    HTTP Status code from Boto3 Response Exception

    """

    def __init__(self, error: ClientError):
        self._error = error

    @property
    def error_code(self):
        return self._error['Error']['Code']

    @property
    def request_id(self):
        return self._error['ResponseMetadata']['RequestId']

    @property
    def message(self):
        return self._error.response["Error"]["Message"]

    @property
    def http_status_code(self):
        return self._error.response['ResponseMetadata']['HTTPStatusCode']


# TODO: the access to this service must be restricted to CSM users only (?)
class S3BucketService(ApplicationService):
    """
    Service for S3 account management
    """

    def __init__(self, s3plugin: S3Plugin):
        self._s3plugin = s3plugin

        self._s3_connection_config = S3ConnectionConfig()
        self._s3_connection_config.host = Conf.get(const.CSM_GLOBAL_INDEX, "S3.host")
        self._s3_connection_config.port = Conf.get(const.CSM_GLOBAL_INDEX, "S3.s3_port")
        self._s3_connection_config.max_retries_num = Conf.get(const.CSM_GLOBAL_INDEX,
                                                              "S3.max_retries_num")

    async def get_s3_client(self, s3_session: S3Credentials) -> S3Client:
        """
        Create S3 Client object for S3 session user

        :param s3_session: S3 Account information
        :type s3_session: S3Credentials
        :return:
        """
        # TODO: it should be a common method for all services
        return self._s3plugin.get_s3_client(access_key=s3_session.access_key,
                                            secret_key=s3_session.secret_key,
                                            connection_config=self._s3_connection_config,
                                            session_token=s3_session.session_token)

    @Log.trace_method(Log.INFO)
    async def create_bucket(self, s3_session: S3Credentials,
                            bucket_name: str) -> Union[Response, Bucket]:
        """
        Create new bucket by given name

        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :param bucket_name: name of bucket for creation
        :type bucket_name: str
        :return:
        """
        Log.debug(f"Requested to create bucket by name = {bucket_name}")
        try:
            s3_client = await self.get_s3_client(s3_session)  # type: S3Client
            bucket = await s3_client.create_bucket(bucket_name)
        except ClientError as e:
            # TODO: distinguish errors when user is not allowed to get/delete/create buckets
            Log.debug(f'{e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))

        return bucket  # Can be None

    @Log.trace_method(Log.INFO)
    async def list_buckets(self, s3_session: S3Credentials) -> dict:
        """
        Retrieve the full list of existing buckets

        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :return:
        """
        # TODO: pagination can be added later
        Log.debug(f"Retrieve the whole list of buckets for active user session")
        s3_client = await self.get_s3_client(s3_session)  # type: S3Client
        try:
            bucket_list = await s3_client.get_all_buckets()
        except ClientError as e:
            # TODO: distinguish errors when user is not allowed to get/delete/create buckets
            Log.error(f'Error occured while listing buckets: {e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))

        # TODO: create model for response
        bucket_list = [{"name": bucket.name} for bucket in bucket_list]
        Log.debug(f"List of buckets: {bucket_list}")
        return {"buckets": bucket_list}

    @Log.trace_method(Log.INFO)
    async def delete_bucket(self, bucket_name: str, s3_session: S3Credentials):
        """
        Delete bucket by given name

        :param bucket_name: name of bucket for creation
        :type bucket_name: str
        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :return:
        """
        Log.debug(f"Requested to delete bucket by name = {bucket_name}")

        s3_client = await self.get_s3_client(s3_session)  # TODO: s3_client can't be returned

        try:
            # NOTE: returns None if deletion is successful
            await s3_client.delete_bucket(bucket_name)
        except ClientError as e:
            Log.error(f'Error in deleting bucket: {e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))

    @Log.trace_method(Log.INFO)
    async def get_bucket_policy(self, s3_session: S3Credentials,
                                bucket_name: str) -> dict:
        """
        Retrieve the policy of existing bucket

        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :param bucket_name: s3 bucket name
        :type bucket_name: str
        :returns: A dict of bucket policy
        """
        Log.debug(f"Retrieve bucket bucket by name = {bucket_name}")
        s3_client = await self.get_s3_client(s3_session)  # type: S3Client
        try:
            bucket_policy = await s3_client.get_bucket_policy(bucket_name)
        except ClientError as e:
            Log.debug(f'{e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))
        return bucket_policy

    @Log.trace_method(Log.INFO)
    async def put_bucket_policy(self, s3_session: S3Credentials, bucket_name: str,
                                policy: dict) -> dict:
        """
        Create or update the policy of existing bucket

        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :param bucket_name: s3 bucket name
        :type bucket_name: str
        :returns: Success message
        """
        Log.debug(
            f"Requested to put bucket policy for bucket name = {bucket_name}")
        s3_client = await self.get_s3_client(s3_session)  # type: S3Client
        try:
            bucket_policy = await s3_client.put_bucket_policy(bucket_name, policy)
        except ClientError as e:
            Log.debug(f'{e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))
        return {"message": "Bucket Policy Updated Successfully."}

    @Log.trace_method(Log.INFO)
    async def delete_bucket_policy(self, s3_session: S3Credentials,
                                bucket_name: str) -> dict:
        """
        Delete the policy of existing bucket

        :param s3_session: s3 user session
        :type s3_session: S3Credentials
        :param bucket_name: s3 bucket name
        :type bucket_name: str
        :returns: Success message
        """
        Log.debug(
            f"Requested to delete bucket policy for bucket name = {bucket_name}")
        s3_client = await self.get_s3_client(s3_session)  # type: S3Client
        try:
            bucket_policy = await s3_client.delete_bucket_policy(bucket_name)
        except ClientError as e:
            Log.debug(f'{e}')
            error = Boto3Error(e)
            return Response(rc=error.http_status_code, output=str(error.message))
        return {"message": "Bucket Policy Deleted Successfully."}


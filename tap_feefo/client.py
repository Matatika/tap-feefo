"""REST client handling, including FeefoStream base class."""

from __future__ import annotations

import typing as t
from functools import cached_property
from http import HTTPStatus

from singer_sdk.exceptions import RetriableAPIError
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream
from typing_extensions import override

from tap_feefo.auth import FeefoAuthenticator

if t.TYPE_CHECKING:
    from requests import Response
    from singer_sdk.helpers.types import Context


class FeefoStream(RESTStream):
    """Feefo stream class."""

    url_base = "https://api.feefo.com/api/20"

    @override
    @cached_property
    def authenticator(self):
        client_id = "client_id" in self.config
        client_secret = "client_secret" in self.config

        if client_id and client_secret:
            return FeefoAuthenticator.create_for_stream(self)

        if client_id:
            self.logger.warning(
                "Client ID provided without a client secret, proceeding without "
                "authentication"
            )
        elif client_secret:
            self.logger.warning(
                "Client secret provided without a client ID, proceeding without "
                "authentication"
            )

        return None

    @override
    def get_new_paginator(self):
        return BasePageNumberPaginator(1)

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ):
        params = super().get_url_params(context, next_page_token)
        params["merchant_identifier"] = self.config["merchant_id"]
        params["page_size"] = 100
        params["page"] = next_page_token

        return params

    @override
    def validate_response(self, response: Response):
        if (
            response.status_code == HTTPStatus.FORBIDDEN
            and not self.authenticator.is_token_valid()
        ):
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)

        return super().validate_response(response)

    @override
    def response_error_message(self, response: Response):
        msg = super().response_error_message(response)

        if (
            response.status_code == HTTPStatus.FORBIDDEN
            and self.authenticator.is_token_valid()
        ):
            msg += (
                "\n"
                "Check the provided client credentials are valid for the merchant "
                "'{}'".format(self.config["merchant_id"])
            )

        return msg

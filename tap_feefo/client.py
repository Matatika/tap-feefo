"""REST client handling, including FeefoStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BasePageNumberPaginator
from singer_sdk.streams import RESTStream
from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class FeefoStream(RESTStream):
    """Feefo stream class."""

    url_base = "https://api.feefo.com/api/20"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="x-api-key",
            value=self.config.get("auth_token", ""),
            location="header",
        )

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

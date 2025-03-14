"""Feefo tap class."""

from __future__ import annotations

from datetime import date, datetime, timezone

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from typing_extensions import override

from tap_feefo import streams


class TapFeefo(Tap):
    """Feefo tap class."""

    name = "tap-feefo"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "merchant_id",
            th.StringType,
            required=True,
            title="Merchant ID",
            description="Feefo merchant ID (e.g. `example-retail-merchant`)",
        ),
        th.Property(
            "client_id",
            th.StringType,
            title="Client ID",
            description="Feefo OAuth 2.0 client ID",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            title="Client secret",
            description="Feefo OAuth 2.0 client secret",
            secret=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description=(
                "Timestamp in ISO 8601 format to get data from (inclusive) - "
                "defaults to the first day/month of the current year"
            ),
            title="Start date",
            default=date(datetime.now(timezone.utc).year, 1, 1).isoformat(),
        ),
    ).to_dict()

    @override
    def discover_streams(self):
        return [
            streams.ReviewsStream(self),
            streams.ProductRatingsStream(self),
        ]


if __name__ == "__main__":
    TapFeefo.cli()

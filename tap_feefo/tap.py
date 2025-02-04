"""Feefo tap class."""

from __future__ import annotations

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
            description="Feefo merchant identify (e.g. `example-retail-merchant`)",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Timestamp in ISO 8601 format to get data from (inclusive)",
            title="Start date",
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

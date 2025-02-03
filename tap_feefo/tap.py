"""Feefo tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
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

    def discover_streams(self) -> list[streams.FeefoStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.GroupsStream(self),
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    TapFeefo.cli()

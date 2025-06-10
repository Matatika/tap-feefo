"""Tests standard tap features using the built-in SDK tests library."""

from datetime import datetime, timezone

from singer_sdk.testing import get_tap_test_class

from tap_feefo.tap import TapFeefo

SAMPLE_CONFIG = {
    "merchant_id": "example-retail-merchant",
    "start_date": datetime.min.replace(tzinfo=timezone.utc).isoformat(),
}


# Run standard built-in tap tests from the SDK:
TestTapFeefo = get_tap_test_class(
    tap_class=TapFeefo,
    config=SAMPLE_CONFIG,
)

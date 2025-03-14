"""Tests standard tap features using the built-in SDK tests library."""

from datetime import datetime

from singer_sdk.testing import get_tap_test_class

from tap_feefo.tap import TapFeefo

SAMPLE_CONFIG = {
    "start_date": datetime.min.isoformat(),
}


# Run standard built-in tap tests from the SDK:
TestTapFeefo = get_tap_test_class(
    tap_class=TapFeefo,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.

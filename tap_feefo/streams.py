"""Stream type classes for tap-feefo."""

from __future__ import annotations

from datetime import datetime, timezone

from typing_extensions import override

from tap_feefo.client import FeefoStream
from tap_feefo.schemas.product import ProductRatingObject
from tap_feefo.schemas.review import ReviewObject


class ReviewsStream(FeefoStream):
    """Define reviews stream."""

    name = "reviews"
    path = "/reviews/all"
    records_jsonpath = "$.reviews[*]"
    replication_key = "last_updated_date"
    schema = ReviewObject.to_dict()

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)

        delta = datetime.now(timezone.utc) - self.get_starting_timestamp(context)

        if delta.days < 30:  # noqa: PLR2004
            since_updated_period = "month"
        elif delta.days < 365:  # noqa: PLR2004
            since_updated_period = "year"
        else:
            since_updated_period = "all"

        params["since_updated_period"] = since_updated_period

        return params


class ProductRatingsStream(FeefoStream):
    """Define product ratings stream."""

    name = "product_ratings"
    path = "/products/ratings"
    records_jsonpath = "$.products[*]"
    primary_keys = ("sku",)
    schema = ProductRatingObject.to_dict()

    @override
    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        params["page_size"] = 1000
        params["since_period"] = "all"
        params["review_count"] = True

        return params

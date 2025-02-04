"""Stream type classes for tap-feefo."""

from __future__ import annotations

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
    def get_url_params(self, *args, **kwargs):
        params = super().get_url_params(*args, **kwargs)
        params["since_updated_period"] = "all"

        return params


class ProductRatingsStream(FeefoStream):
    """Define product ratings stream."""

    name = "product_ratings"
    path = "/products/ratings"
    records_jsonpath = "$.products[*]"
    primary_keys = ("sku",)
    schema = ProductRatingObject.to_dict()

    @override
    def get_url_params(self, *args, **kwargs):
        params = super().get_url_params(*args, **kwargs)
        params["page_size"] = 1000
        params["since_period"] = "all"
        params["review_count"] = True

        return params

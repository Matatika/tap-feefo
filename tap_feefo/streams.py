"""Stream type classes for tap-feefo."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from singer_sdk import typing as th
from typing_extensions import override

from tap_feefo.client import FeefoStream
from tap_feefo.schemas.product import ProductRatingObject
from tap_feefo.schemas.review import ReviewObject

REVIEW_ID_KEY = "_id"


class ReviewsStream(FeefoStream):
    """Define reviews stream."""

    name = "reviews"
    path = "/reviews/all"
    records_jsonpath = "$.reviews[*]"
    primary_keys = (REVIEW_ID_KEY,)
    replication_key = "last_updated_date"
    schema = th.PropertiesList(
        *ReviewObject,
        th.Property(REVIEW_ID_KEY, th.StringType),
    ).to_dict()

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

    @override
    def post_process(self, row, context=None):
        feedback_ids = []

        if service := row.get("service"):
            feedback_ids.append(service["id"])

        if products := row.get("products"):
            feedback_ids.extend(p["id"] for p in products)

        if not feedback_ids:
            self.logger.warning(
                "Malformed review: no feedback IDs to generate a review "
                "ID with, skipping"
            )
            return None

        self.logger.debug(
            "Generating review ID from feedback IDs: %s",
            ", ".join(feedback_ids),
        )

        review_id = hashlib.md5(
            "".join(feedback_ids).encode(),
            usedforsecurity=False,
        ).hexdigest()

        self.logger.debug("Generated review ID: %s", review_id)

        row[REVIEW_ID_KEY] = review_id
        return row


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

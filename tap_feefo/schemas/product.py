"""Schema definitions for product objects."""

from singer_sdk import typing as th

from tap_feefo.schemas import (
    AggregatableScoresProperty,
    CustomProperty,
    MediaProperty,
    ModerationStatusProperty,
    RatingProperty,
    SocialProperty,
)

ProductObject = th.PropertiesList(
    RatingProperty,
    th.Property("id", th.StringType),
    th.Property("review", th.StringType),
    CustomProperty,
    MediaProperty,
    SocialProperty,
    ModerationStatusProperty,
    AggregatableScoresProperty,
    th.Property(
        "product",
        th.PropertiesList(
            th.Property("title", th.StringType),
            th.Property("sku", th.StringType),
            th.Property("url", th.URIType),
            th.Property("reviews_url", th.URIType),
            th.Property("parent_sku", th.StringType),
            th.Property("image_url", th.URIType),
        ),
    ),
    th.Property(
        "attributes",
        th.ArrayType(
            th.PropertiesList(
                *RatingProperty.wrapped,
                th.Property("name", th.StringType),
                th.Property("key", th.StringType),
            )
        ),
    ),
    th.Property("created_at", th.DateTimeType),
    th.Property("helpful_votes", th.IntegerType),
)

ProductRatingObject = th.PropertiesList(
    th.Property("rating", th.NumberType),
    th.Property("sku", th.StringType),
    th.Property("review_count", th.IntegerType),
)

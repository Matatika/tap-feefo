"""Schema definitions for review objects."""

from singer_sdk import typing as th

from tap_feefo.schemas import (
    AggregatableScoresProperty,
    MediaProperty,
    RatingProperty,
    SocialProperty,
)
from tap_feefo.schemas.product import ProductObject

ReviewObject = th.PropertiesList(
    th.Property(
        "merchant",
        th.PropertiesList(
            th.Property("identifier", th.StringType),
        ),
    ),
    th.Property("url", th.URIType),
    SocialProperty,
    th.Property(
        "customer",
        th.PropertiesList(
            th.Property("display_name", th.StringType),
            th.Property("display_location", th.StringType),
        ),
    ),
    th.Property(
        "service",
        th.PropertiesList(
            RatingProperty,
            th.Property("id", th.StringType),
            th.Property("title", th.StringType),
            th.Property("review", th.StringType),
            MediaProperty,
            th.Property(
                "moderation_status",
                th.StringType,
                allowed_values=["pending", "published", "rejected"],
            ),
            AggregatableScoresProperty,
            th.Property("created_at", th.DateTimeType),
            th.Property("helpful_votes", th.IntegerType),
        ),
    ),
    th.Property("products", th.ArrayType(ProductObject)),
    th.Property("locale", th.StringType),
    th.Property("products_purchased", th.ArrayType(th.StringType)),
    th.Property("last_updated_date", th.DateTimeType),
)

"""Schema definitions for review objects."""

from singer_sdk import typing as th

from tap_feefo.schemas import (
    AggregatableScoresProperty,
    CustomProperty,
    MediaProperty,
    ModerationStatusProperty,
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
    th.Property(
        "tags",
        th.ArrayType(
            th.PropertiesList(
                th.Property(
                    "type",
                    th.StringType,
                    allowed_values=["SALE"],
                ),
                th.Property("key", th.StringType),
                th.Property("values", th.ArrayType(th.StringType)),
            )
        ),
    ),
    th.Property("url", th.URIType),
    SocialProperty,
    th.Property(
        "customer",
        th.PropertiesList(
            th.Property("name", th.StringType),
            th.Property("email", th.EmailType),
            th.Property("mobile", th.StringType),
            th.Property("display_name", th.StringType),
            th.Property("display_location", th.StringType),
            th.Property("order_ref", th.StringType),
            th.Property("customer_ref", th.StringType),
        ),
    ),
    th.Property(
        "service",
        th.PropertiesList(
            RatingProperty,
            th.Property("id", th.StringType),
            th.Property("title", th.StringType),
            th.Property("review", th.StringType),
            CustomProperty,
            MediaProperty,
            ModerationStatusProperty,
            AggregatableScoresProperty,
            th.Property("created_at", th.DateTimeType),
            th.Property("helpful_votes", th.IntegerType),
        ),
    ),
    th.Property("products", th.ArrayType(ProductObject)),
    th.Property(
        "nps",
        th.PropertiesList(
            RatingProperty,
            th.Property("created_at", th.DateTimeType),
            th.Property("reason", th.DateTimeType),
        ),
    ),
    th.Property("locale", th.StringType),
    th.Property("products_purchased", th.ArrayType(th.StringType)),
    th.Property("last_updated_date", th.DateTimeType),
)

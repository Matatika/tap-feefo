"""Schema definitions for tap-feefo."""

from singer_sdk import typing as th

RatingProperty = th.Property(
    "rating",
    th.PropertiesList(
        th.Property("min", th.IntegerType),
        th.Property("max", th.IntegerType),
        th.Property("rating", th.IntegerType),
    ),
)

SocialProperty = th.Property(
    "social",
    th.PropertiesList(
        th.Property("facebook", th.URIType),
        th.Property("twitter", th.URIType),
    ),
)

MediaProperty = th.Property(
    "media",
    th.ArrayType(
        th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property(
                "type",
                th.StringType,
                allowed_values=["PHOTO", "VIDEO"],
            ),
            th.Property("url", th.URIType),
            th.Property("carouselUrl", th.URIType),
            th.Property("thumbnail", th.URIType),
            th.Property("caption", th.StringType),
            SocialProperty,
            th.Property("removed", th.BooleanType),
            th.Property("helpful_votes", th.IntegerType),
        )
    ),
)

AggregatableScoresProperty = th.Property(
    "aggregatableScores",
    th.ArrayType(
        th.PropertiesList(
            th.Property("questionIdentifierKey", th.StringType),
            th.Property("score", th.IntegerType),
            th.Property("aggregatableScoreDisplayType", th.StringType),  # PERCENTAGE
            th.Property("type", th.StringType),  # OVERALL, FIT
        )
    ),
)

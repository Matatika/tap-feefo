"""Feefo Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from typing_extensions import override


class FeefoAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Feefo."""

    @override
    @property
    def oauth_request_body(self):
        return {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(cls, stream) -> FeefoAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint="https://api.feefo.com/api/oauth/v2/token",
        )

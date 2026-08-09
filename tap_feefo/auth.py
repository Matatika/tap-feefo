"""Feefo Authentication."""

from __future__ import annotations

from functools import cached_property

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from typing_extensions import override


class FeefoAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Feefo."""

    @override
    @property
    def oauth_request_body(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

    @cached_property
    def _has_credentials(self) -> bool:
        """Check that a complete pair of client credentials is available.

        A warning is logged once if only one of the two credentials is
        available.

        Returns:
            True if both a client ID and a client secret are available.
        """
        if self.client_id and self.client_secret:
            return True

        if self.client_id:
            self.logger.warning(
                "Client ID provided without a client secret, proceeding without "
                "authentication"
            )
        elif self.client_secret:
            self.logger.warning(
                "Client secret provided without a client ID, proceeding without "
                "authentication"
            )

        return False

    @classmethod
    def create_for_stream(cls, stream) -> FeefoAuthenticator:
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            auth_endpoint="https://api.feefo.com/api/oauth/v2/token",
            client_id=stream.config.get("client_id"),
            client_secret=stream.config.get("client_secret"),
        )

    @override
    def authenticate_request(self, request):
        if self._has_credentials:
            return super().authenticate_request(request)

        return request

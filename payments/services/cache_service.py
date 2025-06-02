from django.core.cache import cache
from ..constants import DURATION_ONE_HOUR_IN_SECS


class OrganizationCashService:
    """Service for caching AboutUsInfo data."""

    @staticmethod
    def get_cache_key(inn: str) -> str:
        """Generate cache key based on language."""
        return f'_organization_{inn}'

    @staticmethod
    def get_organization_info(inn):
        """Retrieve 'AboutUs' data from cache or database for a specific language."""
        from ..models import Organization

        cache_key = OrganizationCashService.get_cache_key(inn)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        organization = Organization.objects.filter(inn=inn).first()
        if not organization:
            return None

        return OrganizationCashService.refresh_cache(organization, inn)

    @staticmethod
    def refresh_cache(instance, inn: str) -> dict:
        """Update the cache with the current data from the instance."""
        from ..serializers import OrganizationBalanceSerializer

        cache_key = OrganizationCashService.get_cache_key(inn)

        serializer = OrganizationBalanceSerializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=DURATION_ONE_HOUR_IN_SECS)
        return data

    @staticmethod
    def clear_cache(inn: str) -> None:
        """Clear the cache. If language is None, clear all language-specific caches."""
        cache.delete(OrganizationCashService.get_cache_key(inn))

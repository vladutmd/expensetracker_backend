import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)

class UserSpecificSlugRelatedField(serializers.SlugRelatedField):

    def get_queryset(self):
        request = self.context.get("request")
        queryset = super(UserSpecificSlugRelatedField, self).get_queryset()

        if queryset is None:
            return None

        if request and not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        
        return queryset
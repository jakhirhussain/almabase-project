from rest_framework import serializers
from website.models import UserRecords, Site

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'

class UserRecordsSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())

    class Meta:
        model = UserRecords
        fields = '__all__'


class InitiateTaskSerializer(serializers.Serializer):
    task_name = serializers.CharField(required=True)

    def check_site_id(self, site_id):
        if not Site.objects.filter(id=site_id).exists():
            raise serializers.ValidationError("site id not found")
        return site_id
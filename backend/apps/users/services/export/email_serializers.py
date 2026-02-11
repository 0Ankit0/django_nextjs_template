from rest_framework import serializers


class UserDataExportEmailBaseSerializer(serializers.Serializer):
    email = serializers.CharField()
    export_url = serializers.CharField()


class UserDataExportEmailSerializer(serializers.Serializer):
    data = UserDataExportEmailBaseSerializer()  # type: ignore[assignment]


class AdminDataExportEmailSerializer(serializers.Serializer):
    data = UserDataExportEmailBaseSerializer(many=True)  # type: ignore[assignment]

# Thirdparty Libraries
from rest_framework.serializers import ModelSerializer


# #################################################################################### #
class BooksBaseSerializer(ModelSerializer):
    model = None

    def create(self, validated_data):

        return self.model.objects.create(**validated_data)

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

from rest_framework import generics, permissions

from .serializers import CustomUserProfileSerializers


class CustomUserProfileListView(generics.RetrieveAPIView):
    serializer_class = CustomUserProfileSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

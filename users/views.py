from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import SignupSerializer
from .permissions import IsManager
from .models import CustomUser


class SignupViewset(ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes = [IsAuthenticated, IsManager]

    @api_view(
        [
            "POST",
        ]
    )
    def signup_view(self, request):
        serializer = SignupSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["response"] = "Successfully registered a new user."
            data["email"] = user.email
            data["user_type"] = user.user_type
        else:
            data = serializer.errors
        return Response(data)

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"User '{instance}' deleted successfully."},
            status=status.HTTP_200_OK,
        )

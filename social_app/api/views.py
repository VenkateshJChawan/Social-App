from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import views
from rest_framework.throttling import UserRateThrottle
from .models import FriendRequest, Friendship
from .serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer
from .serializers import UserSignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


User = get_user_model()

# Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchPagination(PageNumberPagination):
    page_size = 10


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if not query:
            return User.objects.none()
        
        # Search for exact email match or name containing the search keyword
        queryset = User.objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        ).distinct()
        
        return queryset

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, user_id):
        # to_user = User.objects.get(id=user_id)
        from_user = request.user

        try:
            to_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

class RespondFriendRequestView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_id = request.data.get('request_id')
        response = request.data.get('response')


        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if response not in ['accepted', 'rejected']:
            return Response({'detail': 'Invalid response.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.status = response
        friend_request.save()

        if response == 'accepted':
            friendship1, created1 = Friendship.objects.get_or_create(user1=request.user, user2=friend_request.from_user)
            friendship2, created2 = Friendship.objects.get_or_create(user1=friend_request.from_user, user2=request.user)
            print(f"Created friendship records: {friendship1}, {friendship2}")

        serializer = FriendRequestSerializer(friend_request)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_ids = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).values_list('user1', 'user2')

        friend_ids = list(set([id for ids in friend_ids for id in ids if id != user.id]))

        return User.objects.filter(id__in=friend_ids)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

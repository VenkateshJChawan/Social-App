from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/<int:user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='friends-list'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]

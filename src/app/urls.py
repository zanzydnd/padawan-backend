from django.urls import path
from django.contrib.staticfiles.urls import static
from django.conf import settings
# from .views import IndexView
from app.views import SignUpView, CustomLoginView, logout_view, IndexView, ClassroomListView, ClassroomDetailView, \
    AssignmentListView, AssignmentDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('auth/', CustomLoginView.as_view(), name='auth'),
    path("logout/", logout_view, name="logout_view"),

    path("classrom/", ClassroomListView.as_view(), name="classroom_list"),
    path("classrom/<str:unique_code>/", ClassroomDetailView.as_view(), name="classroom_detail"),

    path("assignment/", AssignmentListView.as_view(), name="assignment_list"),
    path("assignment/<int:pk>/", AssignmentDetailView.as_view(), name="assignment_detail")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
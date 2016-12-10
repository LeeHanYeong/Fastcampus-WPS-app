from rest_framework.routers import DefaultRouter
from course import apis

router = DefaultRouter()
router.register(r'course', apis.CourseViewSet)
router.register(r'lecture-section', apis.LectureSectionViewSet)
urlpatterns = router.urls

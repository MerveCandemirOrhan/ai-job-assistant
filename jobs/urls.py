from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("cv/upload/", views.upload_cv, name="upload_cv"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("cv/<int:cv_id>/", views.cv_detail, name="cv_detail"),
    path("my-cvs/", views.my_cvs, name="my_cvs"),
    path("cv/<int:cv_id>/file/", views.download_cv, name="download_cv"),
]
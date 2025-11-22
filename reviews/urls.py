from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/', views.AddReviewView.as_view(), name='add_review'),
    path('<int:review_id>/helpful/', views.MarkHelpfulView.as_view(), name='mark_helpful'),
    path('<int:review_id>/images/', views.AddReviewImageView.as_view(), name='add_review_image'),
]

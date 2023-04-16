from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import signup_view
from .views import signout_view
from .views import get_dealer_details

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # URL pattern for about us page
    path('about/', views.about_view, name='about'),
    # URL pattern for contact us page
    path('contact/', views.contact_view, name='contact'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),  # Add login view URL pattern

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),
    path('signout/', views.signout_view, name='signout'),
    path('dealerreview/<int:dealer_id>/', get_dealer_details, name='dealer_details'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


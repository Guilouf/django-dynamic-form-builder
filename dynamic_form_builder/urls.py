from django.urls import path

from dynamic_form_builder import views

urlpatterns = [
    path('<int:template_pk>', views.template_form_view, name='template'),
]

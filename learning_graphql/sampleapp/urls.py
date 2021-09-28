from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from schema import schema

urlpatterns = [
    path('snippets/', include('snippets.urls', namespace='snippets')),
    path('graphql/', GraphQLView.as_view(graphql=True,schema=schema)),
    path('admin/', admin.site.urls),
]

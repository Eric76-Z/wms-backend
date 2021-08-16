"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

import xadmin
from wms.settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', xadmin.site.urls, name='xadmin'),
    path('api/workstation/', include('workstation.urls')),
    path('api/myuser/', include('myuser.urls')),
    path('docs/', include_docs_urls(title="WMS API 文档", description="描述信息")),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]

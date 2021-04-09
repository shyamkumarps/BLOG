

from django.contrib import admin
from django.urls import path, include




urlpatterns = [
   
    path('admin/', admin.site.urls),
    

    # REST_FRAMEWORK URL 
    path('api/blog/', include('blog.api.urls', 'blog_api')),
    path('api/account/', include('account.api.urls', 'account_api')),

]

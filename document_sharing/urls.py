from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from file_upload import views
urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('accounts.api.urls')),

    path('', views.Home.as_view(), name='home'),
    path('books/', views.book_list, name='book_list'),
    path('upload/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/', views.delete_book, name='delete_book'),

    path('books/', views.BookListView.as_view(), name='class_book_list'),
    path('books/upload/', views.UploadBookView.as_view(), name='class_upload_book'),

    url(r'^mail/', include('emailattachment.urls')),

]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

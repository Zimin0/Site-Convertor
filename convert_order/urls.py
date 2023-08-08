from django.urls import path
from convert_order.views import clear_main, files_main, info, video

app_name = 'convert_order'

urlpatterns = [
    path('', clear_main, name='clear_main'),
    path('info/', info, name='info'),
    path('video/<int:video_id>', video, name='video'),
    path('upload/<str:order_id>/', files_main, name='files_main'),  
]

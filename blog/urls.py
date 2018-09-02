from django.conf.urls import url
from . import views

urlpatterns = [
	# post views
	#url(r'^$', views.post_list, name='post_list'),
	url(r'^$', views.PostListView.as_view(), name='post_list'),
	url(r'^(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
	url(r'^badbrowser/$', views.ErrorJsView.as_view(), name='noscript'),
]
handler404 = 'trydjango18.views.custom_404'
handler400 = 'views.custom_400'
handler500 = 'views.custom_500'

# -*- coding: utf-8 -*-

from django.conf.urls import url
from adminka import views, gallery, do, pages_temp




#/adminka/

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^media/$', gallery.media_all, name='media_all'),
    url(r'^media/add/$', gallery.media_add, name='media_add'),
    url(r'^media/search/$', gallery.media_search, name='media_search'),
    url(r'^media/found/$', gallery.media_found, name='media_found'),
    url(r'^media/edit/(?P<img_id>\d+)/$', gallery.image_edit, name='image_edit'),
    url(r'^media/delete/(?P<img_id>\d+)/$', gallery.media_delete, name='media_delete'),


    url(r'^users/$', views.users_all, name='users_all'),
    url(r'^users/add/$', views.users_add_user, name='users_add_user'),
    url(r'^user/(?P<user_id>\d+)/$', views.users_show_user, name='users_show_user'),
    url(r'^myprofile/$', views.my_profile, name='my_profile'),
    url(r'^profile/change/$', views.user_profile_change, name='user_profile_change'),
    url(r'^profile/add/(?P<oper_name>\w+)/$', views.profile_change_part, name='profile_change_part'),
    url(r'^profile/del/(?P<oper_name>\w+)/(?P<one_id>\d+)/$', views.profile_del_part, name='profile_del_part'),
    url(r'^perms/permissions/$', views.adm_perms_personal, name='adm_perms_personal'),
    url(r'^user/change/password/$', views.user_change_password, name='user_change_password'),

    url(r'^pages/temp/$', pages_temp.page_temp_edit, name='page_main_edit'),
    url(r'^edittemp/contacts/$', pages_temp.edit_temp_contacts, name='edit_temp_contacts'),
    url(r'^edittemp/news/(?P<news_id>\d+)/$', pages_temp.edit_temp_news, name='edit_temp_news'),
    url(r'^service/edit/$', pages_temp.page_temp_service_edit, name='page_temp_service_edit'),
    url(r'^service/(?P<service_id>\d+)/delete/$', pages_temp.page_temp_service_delete, name='page_temp_service_delete'),
    url(r'^service/add/$', pages_temp.page_temp_service_add, name='page_temp_service_add'),
    url(r'^media/edittemp/(?P<img_id>\d+)/$', gallery.image_edit_temp, name='image_edit_temp'),
    # url(r'^pages/main/$', views.page_main_edit, name='page_main_edit'),
    url(r'^do1/$', do.do_1, name='do_1'),
    url(r'^do2/$', do.do_2, name='do_2'),

]

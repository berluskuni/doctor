from django.contrib import admin
from .models import Contact, Service, Gallery, News


class ContactAdmin(admin.ModelAdmin):
    list_display = ['clinic_name', 'clinic_service_one', 'clinic_service_two', 'phone_one', 'phone_two',
                    'time_work_one_hours_begin', 'time_work_one_minute_begin', 'time_work_one_hours_end',
                    'time_work_one_minute_end', 'time_work_two_hours_begin', 'time_work_two_minute_begin',
                    'time_work_two_hours_end', 'time_work_two_minute_end', 'time_work_three',
                    'address_dig', 'address_street']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'label']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'preview', 'label']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_news', 'news_data_day', 'news_data_month', 'description_news', 'img_news']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(News, NewsAdmin)

# Register your models here.

from gettext import gettext

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.template.response import TemplateResponse
from apps.users.models import CustomUser, Profile
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404


class ProfilesInlineAdmin(admin.StackedInline):
    model = Profile


class CustomFilter(admin.SimpleListFilter):
    title = gettext('Возраст аккаунта')
    parameter_name = 'custom_filter'

    def lookups(self, request, model_admin):
        return (
            ('option1', gettext("Молодые")),
            ('option2', gettext("Давние"))
        )

    def queryset(self, request, queryset):
        if self.value() == 'option1':
            return queryset.order_by("-date_joined")
        if self.value() == 'option2':
            return queryset.order_by("date_joined")


class CustomUserAdmin(PermissionRequiredMixin, UserAdmin):
    model = CustomUser
    readonly_fields = ('full_name',)
    permission_required = ('users.add_post', 'users.delete_post')
    list_display = ('email', 'is_staff', 'is_active', 'full_name')
    list_filter = ('is_staff', 'is_active', CustomFilter)
    inlines = [ProfilesInlineAdmin]

    def full_name(self, obj):
        return obj.first_name + obj.last_name

    def get_urls(self):
        urls = super().get_urls()

        user_urls = [
            path('configuration/', self.get_info),
            path('classes/', self.UserList.as_view())
        ]
        return user_urls + urls

    class UserList(PermissionRequiredMixin, ListView):
        model = CustomUser
        permission_required = 'auth.change_user'

        def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data()
            context.update({"title": gettext("Список пользователей"),
                            "data": CustomUser.objects.all().values()})
            return context

    def get_info(self, request):
        if not request.user.is_authenticated():
            raise Http404
        context = dict(self.admin_site.each_context(request))
        context.update({"title": gettext("Реализация действия")})
        return TemplateResponse(request, "users/admin/testing.html", context)


admin.site.register(CustomUser, CustomUserAdmin)

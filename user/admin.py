from django.contrib import admin
from .models import User, UserProfile

# Register your models here.
admin.site.register(UserProfile)

# 사용 방법은 TabulaInline과 StackedInline 모두 동일
# 둘 다 사용해보고 뭐가 좋은지 비교해보기
# class UserProfileInline(admin.TabulaInline):
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = (
            UserProfileInline,
        )

admin.site.register(User, UserAdmin)
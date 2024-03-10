from django.contrib import admin
from accounts.models import User
from django.contrib.auth.hashers import make_password

class UserResourceAdmin(admin.ModelAdmin):
    search_fields = [
        "email",
        "full_name",
        "is_active"
    ]
    list_per_page = 50
    date_hierarchy = "date_joined"

    def get_list_display(self, request):
        to_be_displayed = [field.name for field in self.model._meta.concrete_fields]
        to_be_displayed.remove("password")

        return to_be_displayed
    
    def save_model(self, request, obj, form, change):
        
        # Hash the password before saving
        if "password" in form.changed_data:
            obj.password = make_password(form["password"].value())

        super().save_model(request, obj, form, change)



admin.site.register(User, UserResourceAdmin)
    
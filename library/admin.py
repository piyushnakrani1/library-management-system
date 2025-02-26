from django.contrib import admin
from .models import User, Book, Loan

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Book, Loan, User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', "date_of_birth", 'is_staff', 'is_superuser')
        
    def clean_is_staff(self):
        is_staff = self.cleaned_data.get('is_staff')
        is_superuser = self.cleaned_data.get('is_superuser')

        if is_superuser and not is_staff:
            raise forms.ValidationError("Admin users must be staff.")
        return is_staff


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'is_staff', 'is_superuser')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'page_count', 'available')
    ordering = ('-id',)
    list_per_page = 30
    
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'returned_at')
    ordering = ('-id',)
    list_per_page = 30
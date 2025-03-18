from django.contrib import admin
from .models import (
    Tenant, TenantColor, ContactPerson, TenantFile,
    Unit, Comment, CommentAttachment
)


class ContactPersonInline(admin.StackedInline):
    model = ContactPerson
    extra = 0


class TenantFileInline(admin.StackedInline):
    model = TenantFile
    extra = 0


@admin.register(TenantColor)
class TenantColorAdmin(admin.ModelAdmin):
    list_display = ("color",)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax_id",
        "address",
        "description",
        "phone",
        "email",
        "bank_name",
        "bik",
        "account_number",
        "correspondent_account",
        "color",
        "created_at"
    )
    inlines = [ContactPersonInline, TenantFileInline]
    search_fields = ("name", "tax_id", "phone", "email")
    list_filter = ("color", "created_at")
    ordering = ("name",)


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "phone", "email", "tenant")
    search_fields = ("name", "phone", "email", "tenant__name")
    list_filter = ("tenant",)
    ordering = ("name",)


@admin.register(TenantFile)
class TenantFileAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant", "uploaded_by", "uploaded_at")
    search_fields = ("name", "tenant__name", "uploaded_by")
    list_filter = ("tenant", "uploaded_at")
    ordering = ("uploaded_at",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "floor",
        "area",
        "height",
        "status",
        "tenant",
        "lease_start",
        "lease_end"
    )
    search_fields = ("number", "tenant__name")
    list_filter = ("floor", "status", "tenant")
    ordering = ("floor", "number")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "created_at", "tenant", "unit")
    search_fields = ("author__username", "text", "tenant__name", "unit__number")
    list_filter = ("created_at", "tenant", "unit")
    ordering = ("-created_at",)


@admin.register(CommentAttachment)
class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ("comment", "file", "uploaded_at")
    search_fields = ("comment__text",)
    list_filter = ("uploaded_at",)
    ordering = ("-uploaded_at",)
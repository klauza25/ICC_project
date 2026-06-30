from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Colonnes affichées dans la liste
    list_display = ('photo_preview', 'username', 'prenom_nom', 'role', 'departement', 'is_active')
    
    # Filtres dans la barre latérale
    list_filter = ('role', 'departement', 'is_staff', 'is_active')
    
    # Barre de recherche
    search_fields = ('username', 'prenom', 'nom', 'email', 'telephone')
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations ICC', {
            'fields': ('role', 'departement', 'prenom', 'nom', 'telephone', 'adresse', 'profession', 'photo')
        }),
    )
    
    # Organisation pour la création d'un utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations ICC', {
            'fields': ('role', 'departement', 'prenom', 'nom', 'telephone', 'photo')
        }),
    )
    
    # Méthode pour afficher la photo dans la liste
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #6366f1;" />',
                obj.photo.url
            )
        else:
            # Afficher les initiales si pas de photo
            initials = ""
            if obj.prenom and obj.nom:
                initials = f"{obj.prenom[0]}{obj.nom[0]}".upper()
            elif obj.prenom:
                initials = obj.prenom[0].upper()
            elif obj.username:
                initials = obj.username[0].upper()
            else:
                initials = "?"
            
            return format_html(
                '<div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px;">{}</div>',
                initials
            )
    photo_preview.short_description = 'Photo'
    photo_preview.allow_tags = True
    
    # Méthode pour afficher le nom complet
    def prenom_nom(self, obj):
        if obj.prenom and obj.nom:
            return f"{obj.prenom} {obj.nom}"
        return obj.username
    prenom_nom.short_description = 'Nom Complet'
    
    # Permettre l'upload de fichiers
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        # Ajouter un aperçu de la photo actuelle si elle existe
        if obj and obj.photo:
            return readonly + ('photo_current',)
        return readonly
    
    def photo_current(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; border-radius: 8px; border: 2px solid #6366f1;" /><br><small>Photo actuelle</small>',
                obj.photo.url
            )
        return "Aucune photo"
    photo_current.short_description = 'Aperçu Photo'
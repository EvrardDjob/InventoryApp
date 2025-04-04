from django.contrib import admin
from . models import Product, Order
from django.contrib.auth.models import Group

#changer le nom Django Administrator en ....
admin.site.site_header = 'Ekd_administrator Management' 

#formater l'affichage de la liste des Produits en un tableau
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','quantity')
    list_filter = ('category',)
    search_fields = ('name', )
    list_editable = ('quantity',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
#admin.site.unregister(Group)
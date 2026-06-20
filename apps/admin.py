from django.contrib import admin

from apps.models import Product, Category, Stream, Transaction, User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass




@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ['title' , 'product' , 'user' , 'visit' , 'new_order' ,  'delivered']



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'type']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'balance', 'coins']


from apps.models import Competition, CompetitionResult

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']

@admin.register(CompetitionResult)
class CompetitionResultAdmin(admin.ModelAdmin):
    list_display = ['rank', 'seller_name', 'sold_amount']



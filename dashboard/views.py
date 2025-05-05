from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProducForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, OuterRef, Subquery
# Create your views here.
"""Subquery est une classe qui permet d'executer une requete à l'interieur d'une autre requête
annotate permet d'ajouter un champ(clé) au dictionnaire de queryset que retournera values('liste_des_champs')"""
#Creation d'une fonction utilitaire 

def get_counts():
    return {
        'orders_count': Order.objects.count(),
        'members_count': User.objects.count(),
        'products_count': Product.objects.count()
    }


@login_required()
def index(request):
    all_order = Order.objects.all()
    orders = Order.objects.values('product__name').annotate(total_quantity = Sum('order_quantity')) #récupère la somme des quantité commander par nom des produits depuis la table Order
    products = Product.objects.all()

    if request.method == 'POST':
        form_order = OrderForm(request.POST)
        if form_order.is_valid():
            instance = form_order.save(commit=False)
            instance.staff = request.user

            #Récuperer le produit concerné par la commande
            product = instance.product
            if product.quantity >= instance.order_quantity:
                product.quantity -= instance.order_quantity
                product.save()
                instance.save() # On sauvegarde la commande ok? 
                messages.success(request, 'Orders List has been updated')
            else:
                messages.error(request, 'Not enough stock for this product.')
            return redirect('dashboard-index')
    else:
        form_order = OrderForm()
    context = {
        'orders':orders,
        'form_order':form_order,
        'products':products,
        'all_order': all_order,
        **get_counts()
    }
    return render(request, 'dashboard/index.html', context)
    
@login_required()
def staff(request):
    members = User.objects.all()

    context = {
        'members':members,
        **get_counts()
    }
    return render(request, 'dashboard/staff.html', context)

@login_required()
def staff_detail(request, pk):
    staff_member = User.objects.get(id = pk)
    context = {
        'staff_member':staff_member
    }
    return render(request, 'dashboard/staff_detail.html', context)

#j'ai une fois en profiter pour mettre la logique d'enregistrement dans le fonction qui est sensé retourner l'ensemble des produits
@login_required()
def product(request):

    #Regroupons les produits pas nom, et par categorie pour eviter les doublons
    items = Product.objects.values('name', 'category').annotate(total_quatity = Sum('quantity'),
     product_id=Subquery(Product.objects.filter(name=OuterRef('name')).values('id')[:1])                                     
    )# OuterRef:fait référence à la valeur du champ name de l'objet dans la requête externe

    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    if request.method == 'POST':
        product_form = ProducForm(request.POST)
        if product_form.is_valid():
            product_name = product_form.cleaned_data.get('name')
            product_category = product_form.cleaned_data.get('category')
            existing_product = Product.objects.filter(name__iexact = product_name, category__iexact = product_category).first()
            if existing_product:
                existing_product.quantity += product_form.cleaned_data.get('quantity')
                existing_product.save()
                messages.success(request, f"{product_name} has been updaded")
            else:
                product_form.save()
                messages.success(request, f"{product_name} has been added")
            return redirect('dashboard-product')
    
    else :
        product_form = ProducForm()
    context = {
        'items':items, 
        'product_form':product_form,
        **get_counts()
    }
    return render(request, 'dashboard/product.html', context)


def product_delete(request, pk):
    item = Product.objects.get(id = pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


def product_update(request, pk):
    item = Product.objects.get(id = pk)
    if request.method == 'POST':
        form = ProducForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProducForm(instance=item)
    context = {
        'form':form,
    }
    return render(request, 'dashboard/product_update.html', context)

@login_required()
def order(request):
    orders = Order.objects.all()
    context = {
        'orders':orders,
        **get_counts()
    }
    return render(request, 'dashboard/order.html', context) 
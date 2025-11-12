from django.shortcuts import render

def home_view(request):
    return render(request, 'demo/home.html')

def about_view(request):
    return render(request, 'demo/about.html')

def products_view(request):
    return render(request, 'demo/products.html')

def contacts_view(request):
    return render(request, 'demo/contacts.html')

def product_detail_view(request, pk):
    # Можно добавить контекст, если нужно
    return render(request, 'demo/product_detail.html', {'pk': pk})

def product_sub_detail_view(request, pk, subpk):
    return render(request, 'demo/product_sub_detail.html', {'pk': pk, 'subpk': subpk})


def term_view(request):
    return render(request, 'demo/term.html')

def privacy_view(request):
    return render(request, 'demo/privacy.html')
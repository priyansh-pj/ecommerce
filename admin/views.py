from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from product.models import *

# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")
    return render(request, "admin/templates/template.html")

@login_required(login_url="login")
def category(request):
    if not request.user.is_superuser:
        return redirect("home")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = Category(name=name, description=description)
        category.save()
        return redirect("admin_category")
    data = {
        "categories": Category.objects.all()
    }
    return render(request, "admin/category/category.html", data)


@login_required(login_url="login")
def subcategory(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_ids = request.POST.getlist("category")

        subcategory = SubCategory(name=name, description=description)
        subcategory.save()

        # Use the set method to add the selected categories
        subcategory.categories.set(category_ids)

        return redirect("admin_subcategory")

    data = {
        "categories": SubCategory.objects.all(),
        "category_list": Category.objects.values('id', 'name'),
    }
    return render(request, "admin/category/sub-category.html", data)


@login_required(login_url="login")
def brands(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_ids = request.POST.getlist("categories")
        print(category_ids)
        brand = Brand(name=name, description=description)
        brand.save()

        for category_id in category_ids:
            brand.categories.add(category_id)

        brand.save()
    data = {
        "brand": Brand.objects.all(),
        "category_list": Category.objects.values('id', 'name'),

    }
    return render(request, "admin/brand/brands.html", data)

@login_required(login_url="login")
def add_products(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        # Get the form data
        features = request.POST.getlist("product_feature[]")
        feature_descriptions = request.POST.getlist("feature_description[]")

        # Create a new Product object
        product = Product.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            brand=Brand.objects.get(id=request.POST.get("brand")),
            category=Category.objects.get(id=request.POST.get("category")),
            sub_category=SubCategory.objects.get(id=request.POST.get("subcategory")),
            original_price=request.POST.get("mrp"),
            price=request.POST.get("price"),
            tags=request.POST.get("tags"),
        )

        # Create ProductFeature objects for each feature
        for feature, description in zip(features, feature_descriptions):
            ProductFeature.objects.create(
                product=product,
                title=feature,
                feature=description
            )

        # Handle product images
        images = request.FILES.getlist("product_image[]")
        for image in images:
            ProductImage.objects.create(product=product, image=image)

    data = {
        "category": Category.objects.values('id', 'name'),
        "subcategory": SubCategory.objects.values('id', 'name'),
        "brand": Brand.objects.values('id', 'name'),
    }
    return render(request, "admin/product/product_create.html", data)

@login_required(login_url="login")
def product(request):
    if not request.user.is_superuser:
        return redirect("home")
    return render(request, "admin/product/product.html")

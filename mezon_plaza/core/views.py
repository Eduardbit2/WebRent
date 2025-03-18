from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, UnitForm
from .models import Unit, Tenant, Comment, CommentAttachment, ContactPerson


@login_required
def unit_list(request):
    units = Unit.objects.select_related('tenant').all()
    return render(request, 'core/unit_list.html', {'units': units})


@login_required
def unit_create(request):
    """Создание нового помещения"""
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:unit_list')
    else:
        form = UnitForm()

    return render(request, 'core/unit_create.html', {'form': form})


@login_required
def tenant_detail(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    form = CommentForm()
    return render(request, 'core/tenant_detail.html', {'tenant': tenant, 'form': form})


@login_required
def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    form = CommentForm()  # Создаем форму и передаем в контекст
    return render(request, 'core/unit_detail.html', {'unit': unit, 'form': form})


@login_required
def add_comment(request, tenant_id=None, unit_id=None):
    """Добавление комментария к арендатору или помещению"""
    tenant = get_object_or_404(Tenant, id=tenant_id) if tenant_id else None
    unit = get_object_or_404(Unit, id=unit_id) if unit_id else None

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.tenant = tenant
            comment.unit = unit
            comment.save()

            # Обрабатываем файлы
            files = request.FILES.getlist('files')
            for file in files:
                CommentAttachment.objects.create(comment=comment, file=file)

            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        form = CommentForm()

    return render(request, "includes/comments.html", {
        "form": form,
        "tenant": tenant,
        "unit": unit
    })


@login_required
def add_contact(request, tenant_id):
    if request.method == "POST":
        tenant = get_object_or_404(Tenant, id=tenant_id)
        ContactPerson.objects.create(
            tenant=tenant,
            name=request.POST.get("name"),
            position=request.POST.get("position"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
        )
    return redirect("core:tenant_detail", tenant_id=tenant_id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import RoadmapItem
from .forms import RoadmapItemForm


@login_required
def roadmap_list(request):
    items = RoadmapItem.objects.filter(
        owner__organization=request.user.organization
    ).select_related('owner').prefetch_related('linked_features')

    status_filter = request.GET.get('status')
    quarter_filter = request.GET.get('quarter')
    if status_filter:
        items = items.filter(status=status_filter)
    if quarter_filter:
        items = items.filter(target_quarter=quarter_filter)

    paginator = Paginator(items, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'roadmap/roadmap_list.html', {
        'page_obj': page_obj,
        'status_choices': RoadmapItem.STATUS_CHOICES,
        'quarter_choices': RoadmapItem.QUARTER_CHOICES,
    })


@login_required
def roadmap_detail(request, pk):
    item = get_object_or_404(
        RoadmapItem.objects.prefetch_related('linked_features'),
        pk=pk,
        owner__organization=request.user.organization
    )
    return render(request, 'roadmap/roadmap_detail.html', {'item': item})


@login_required
def roadmap_create(request):
    if request.method == 'POST':
        form = RoadmapItemForm(request.POST, organization=request.user.organization)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            form.save_m2m()
            messages.success(request, "Roadmap item created.")
            return redirect('roadmap_detail', pk=item.pk)
    else:
        form = RoadmapItemForm(organization=request.user.organization)
    return render(request, 'roadmap/roadmap_form.html', {'form': form})
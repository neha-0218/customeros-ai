from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Feature
from .forms import FeatureForm


@login_required
def feature_list(request):
    features = Feature.objects.filter(
        organization_account__organization=request.user.organization
    ).select_related('organization_account').order_by('-vote_count')

    status_filter = request.GET.get('status')
    if status_filter:
        features = features.filter(status=status_filter)

    paginator = Paginator(features, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'features/feature_list.html', {
        'page_obj': page_obj,
        'status_choices': Feature.STATUS_CHOICES,
    })


@login_required
def feature_detail(request, pk):
    feature = get_object_or_404(
        Feature.objects.select_related('organization_account', 'requested_by'),
        pk=pk,
        organization_account__organization=request.user.organization
    )
    return render(request, 'features/feature_detail.html', {'feature': feature})


@login_required
def feature_create(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST, organization=request.user.organization)
        if form.is_valid():
            feature = form.save(commit=False)
            feature.requested_by = request.user
            feature.save()
            messages.success(request, "Feature request submitted.")
            return redirect('feature_detail', pk=feature.pk)
    else:
        form = FeatureForm(organization=request.user.organization)
    return render(request, 'features/feature_form.html', {'form': form})


@login_required
def feature_vote(request, pk):
    """
    Handles upvoting. POST only — no GET voting,
    prevents vote manipulation via URL refresh.
    """
    if request.method == 'POST':
        feature = get_object_or_404(
            Feature,
            pk=pk,
            organization_account__organization=request.user.organization
        )
        feature.vote_count += 1
        feature.save()
        messages.success(request, f"Voted for '{feature.title}'.")
        return redirect('feature_list')
    return redirect('feature_list')
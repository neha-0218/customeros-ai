from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import HealthScoreSnapshot, RiskFlag
from accounts.models import CustomerAccount


@login_required
def account_health_list(request):
    """
    Shows latest health snapshot per account.
    Using distinct() + ordering by account then snapshot date
    to get one row per account — the most recent snapshot.
    """
    accounts = CustomerAccount.objects.filter(
        organization=request.user.organization,
        is_active=True
    ).prefetch_related('health_snapshots')

    tier_filter = request.GET.get('tier')

    account_health = []
    for account in accounts:
        latest = account.health_snapshots.order_by('-created_at').first()
        if latest:
            if tier_filter and latest.risk_tier != tier_filter:
                continue
            account_health.append({
                'account': account,
                'snapshot': latest,
            })

    account_health.sort(key=lambda x: x['snapshot'].composite_score)

    paginator = Paginator(account_health, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    tier_choices = HealthScoreSnapshot._meta.get_field('risk_tier').choices

    return render(request, 'health/account_health_list.html', {
        'page_obj': page_obj,
        'tier_choices': tier_choices,
    })


@login_required
def account_health_detail(request, pk):
    account = get_object_or_404(
        CustomerAccount,
        pk=pk,
        organization=request.user.organization
    )
    snapshots = account.health_snapshots.order_by('-created_at')[:10]
    latest = snapshots[0] if snapshots else None
    risk_flags = account.risk_flags.order_by('-created_at')

    return render(request, 'health/account_health_detail.html', {
        'account': account,
        'latest': latest,
        'snapshots': snapshots,
        'risk_flags': risk_flags,
    })


@login_required
def risk_flag_list(request):
    flags = RiskFlag.objects.filter(
        customer_account__organization=request.user.organization
    ).select_related('customer_account', 'assigned_to', 'triggering_snapshot')

    status_filter = request.GET.get('status')
    if status_filter:
        flags = flags.filter(status=status_filter)

    flags = flags.order_by('status', '-created_at')
    paginator = Paginator(flags, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'health/risk_flag_list.html', {
        'page_obj': page_obj,
        'status_choices': RiskFlag.STATUS_CHOICES,
    })
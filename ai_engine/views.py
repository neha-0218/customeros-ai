from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AIInsight
from .services import (
    generate_churn_risk_insight,
    generate_feature_demand_insight,
    generate_feedback_theme_insight,
)
from health.models import HealthScoreSnapshot
from accounts.models import CustomerAccount


@login_required
def ai_insight_list(request):
    insights = AIInsight.objects.filter(
        generated_for_user__organization=request.user.organization
    ).exclude(model_used='seed_demo_data').select_related(
        'customer_account', 'generated_for_user'
    ).order_by('-created_at')

    # Also include org-level insights (customer_account=None)
    org_insights = AIInsight.objects.filter(
        customer_account=None,
        generated_for_user=None
    ).exclude(model_used='seed_demo_data').order_by('-created_at')[:20]

    return render(request, 'ai_engine/insight_list.html', {
        'insights': insights[:20],
        'org_insights': org_insights,
    })


@login_required
def ai_insight_detail(request, pk):
    insight = get_object_or_404(AIInsight, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            insight.status = 'accepted'
            insight.save()
            messages.success(request, "Insight accepted.")
        elif action == 'reject':
            insight.status = 'rejected'
            insight.rejection_reason = request.POST.get('rejection_reason', '')
            insight.save()
            messages.info(request, "Insight rejected.")
        return redirect('ai_insight_detail', pk=pk)

    return render(request, 'ai_engine/insight_detail.html', {'insight': insight})


@login_required
def generate_churn_insight(request, account_pk):
    """Triggered by PM clicking 'Generate AI Insight' on an account."""
    account = get_object_or_404(
        CustomerAccount,
        pk=account_pk,
        organization=request.user.organization
    )
    snapshot = account.health_snapshots.order_by('-created_at').first()

    if not snapshot:
        messages.error(request, "No health data available for this account.")
        return redirect('account_health_detail', pk=account_pk)

    try:
        insight = generate_churn_risk_insight(account, snapshot)
        insight.generated_for_user = request.user
        insight.save()
        messages.success(request, f"AI churn risk insight generated for {account.name}.")
        return redirect('ai_insight_detail', pk=insight.pk)
    except ValueError as e:
        messages.error(request, f"AI generation failed: {str(e)}")
        return redirect('account_health_detail', pk=account_pk)


@login_required
def generate_feature_insight(request):
    """Generates org-wide feature demand analysis."""
    try:
        insight = generate_feature_demand_insight(request.user.organization)
        insight.generated_for_user = request.user
        insight.save()
        messages.success(request, "Feature demand insight generated.")
        return redirect('ai_insight_detail', pk=insight.pk)
    except ValueError as e:
        messages.error(request, f"AI generation failed: {str(e)}")
        return redirect('feature_list')


@login_required
def generate_feedback_insight(request):
    """Generates org-wide feedback theme analysis."""
    try:
        insight = generate_feedback_theme_insight(request.user.organization)
        insight.generated_for_user = request.user
        insight.save()
        messages.success(request, "Feedback theme insight generated.")
        return redirect('ai_insight_detail', pk=insight.pk)
    except ValueError as e:
        messages.error(request, f"AI generation failed: {str(e)}")
        return redirect('feedback_list')
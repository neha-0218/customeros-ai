from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Q
from accounts.models import CustomerAccount
from feedback.models import Feedback
from tickets.models import Ticket
from features.models import Feature
from health.models import HealthScoreSnapshot, RiskFlag
from roadmap.models import RoadmapItem
from ai_engine.models import AIInsight
from .forms import SignupForm
from .decorators import role_required

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def dashboard_redirect(request):
    """
    Routes users to a role-specific landing page.
    Right now these are placeholder views — full dashboards get built
    in Phase 23 (Frontend Experience). This just proves role-based
    routing works end to end.
    """
    role = request.user.role
    if role == 'pm':
        return redirect('pm_dashboard')
    elif role == 'analyst':
        return redirect('analyst_dashboard')
    elif role == 'cs_lead':
        return redirect('cs_dashboard')
    else:
        return redirect('pm_dashboard')



@login_required
@role_required(['pm', 'admin'])
def pm_dashboard(request):
    org = request.user.organization

    # Account health summary
    accounts = CustomerAccount.objects.filter(organization=org, is_active=True)
    total_accounts = accounts.count()

    # Get latest snapshot per account
    at_risk = 0
    critical = 0
    for account in accounts:
        latest = account.health_snapshots.order_by('-created_at').first()
        if latest:
            if latest.risk_tier == 'at_risk':
                at_risk += 1
            elif latest.risk_tier == 'critical':
                critical += 1

    # Open risk flags
    open_flags = RiskFlag.objects.filter(
        customer_account__organization=org,
        status__in=['open', 'investigating']
    ).count()

    # Feedback stats
    total_feedback = Feedback.objects.filter(
        customer_account__organization=org
    ).count()

    recent_urgent_feedback = Feedback.objects.filter(
        customer_account__organization=org,
        urgency_score__gte=0.7
    ).select_related('customer_account').order_by('-created_at')[:5]

    # Ticket stats
    open_tickets = Ticket.objects.filter(
        customer_account__organization=org,
        status__in=['open', 'in_progress', 'escalated']
    ).count()

    critical_tickets = Ticket.objects.filter(
        customer_account__organization=org,
        priority='critical',
        status__in=['open', 'in_progress']
    ).count()

    # Feature requests
    top_features = Feature.objects.filter(
        organization_account__organization=org
    ).order_by('-vote_count')[:5]

    # Roadmap
    in_progress_items = RoadmapItem.objects.filter(
        owner__organization=org,
        status='in_progress'
    ).count()

    planned_items = RoadmapItem.objects.filter(
        owner__organization=org,
        status='planned'
    ).count()

    # AI stats
    total_ai_insights = AIInsight.objects.filter(
        generated_for_user__organization=org
    ).exclude(model_used='seed_demo_data').count()

    accepted_insights = AIInsight.objects.filter(
        generated_for_user__organization=org,
        status='accepted'
    ).exclude(model_used='seed_demo_data').count()

    ai_acceptance_rate = round(
        (accepted_insights / total_ai_insights * 100) if total_ai_insights > 0 else 0, 1
    )

    return render(request, 'accounts/pm_dashboard.html', {
        'total_accounts': total_accounts,
        'at_risk': at_risk,
        'critical': critical,
        'open_flags': open_flags,
        'total_feedback': total_feedback,
        'recent_urgent_feedback': recent_urgent_feedback,
        'open_tickets': open_tickets,
        'critical_tickets': critical_tickets,
        'top_features': top_features,
        'in_progress_items': in_progress_items,
        'planned_items': planned_items,
        'ai_acceptance_rate': ai_acceptance_rate,
        'total_ai_insights': total_ai_insights,
    })


@login_required
@role_required(['analyst', 'admin'])
def analyst_dashboard(request):
    return render(request, 'accounts/placeholder_dashboard.html', {'role_label': 'Product Analyst'})


@login_required
@role_required(['cs_lead', 'admin'])
def cs_dashboard(request):
    return render(request, 'accounts/placeholder_dashboard.html', {'role_label': 'Customer Success Lead'})
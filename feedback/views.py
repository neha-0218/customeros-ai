from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Feedback
from .forms import FeedbackForm


@login_required
def feedback_list(request):
    feedback_items = Feedback.objects.filter(
        customer_account__organization=request.user.organization
    ).select_related('customer_account').prefetch_related('themes')

    source_filter = request.GET.get('source')
    status_filter = request.GET.get('status')
    if source_filter:
        feedback_items = feedback_items.filter(source=source_filter)
    if status_filter:
        feedback_items = feedback_items.filter(status=status_filter)

    feedback_items = feedback_items.order_by('-created_at')
    paginator = Paginator(feedback_items, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'feedback/feedback_list.html', {
        'page_obj': page_obj,
        'source_choices': Feedback.SOURCE_CHOICES,
        'status_choices': Feedback.STATUS_CHOICES,
    })


@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(
        Feedback.objects.select_related('customer_account').prefetch_related('themes'),
        pk=pk,
        customer_account__organization=request.user.organization
    )
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, organization=request.user.organization)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submitted_by = request.user
            feedback.save()
            messages.success(request, "Feedback logged successfully.")
            return redirect('feedback_detail', pk=feedback.pk)
    else:
        form = FeedbackForm(organization=request.user.organization)

    return render(request, 'feedback/feedback_form.html', {'form': form})
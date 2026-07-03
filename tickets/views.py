from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Ticket
from .forms import TicketForm


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(
        customer_account__organization=request.user.organization
    ).select_related('customer_account', 'assigned_to')

    priority_filter = request.GET.get('priority')
    status_filter = request.GET.get('status')
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    paginator = Paginator(tickets, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'tickets/ticket_list.html', {
        'page_obj': page_obj,
        'priority_choices': Ticket.PRIORITY_CHOICES,
        'status_choices': Ticket.STATUS_CHOICES,
    })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(
        Ticket.objects.select_related('customer_account', 'assigned_to', 'linked_feature'),
        pk=pk,
        customer_account__organization=request.user.organization
    )
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, organization=request.user.organization)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.assigned_to = request.user
            ticket.save()
            messages.success(request, "Ticket created successfully.")
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(organization=request.user.organization)
    return render(request, 'tickets/ticket_form.html', {'form': form})
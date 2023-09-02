from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, generics
from rest_framework.permissions import IsStaffUser, IsAuthenticated
from django.urls import reverse_lazy
from .models import Card, Purchase
from .serializers import CardSerializer, PurchaseSerializer
from django.views.generic import ListView, View
from .forms import CardSearchForm, PurchaseDeleteForm
from django.views.generic import TemplateView, FormView
from django.http import JsonResponse
from .utils import generate_unique_card_number

def create_card(request):
    if request.method == 'POST':
        owner_name = request.POST['owner_name']

        card_number = generate_unique_card_number()

        # Создаем новую карту в базе данных
        new_card = Card.objects.create(
            owner_name=owner_name,
            card_number=card_number,
            # Другие поля карты...
        )


        return redirect('create-card')

    return render(request, 'create_card.html')

class CardListAPIView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    model = Card


    def get_queryset(self):
        queryset = Card.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class PurchaseListView(ListView):
    model = Purchase
    template_name = 'card/purchase_list.html'
    context_object_name = 'purchases'
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        card_id = self.kwargs['card_id']
        return Purchase.objects.filter(card_id=card_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_id = self.kwargs['card_id']
        context['card_id'] = card_id
        return context

class PurchaseHistoryView(ListView):
    model = Purchase
    template_name = 'card/purchase_history.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        card = get_object_or_404(Card, pk=self.kwargs['card_id'])
        return Purchase.objects.filter(card=card)

class PurchaseDeleteView(TemplateView):
    template_name = 'card/purchase_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        context['form'] = PurchaseDeleteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PurchaseDeleteForm(request.POST)
        if form.is_valid():
            purchases_to_delete = form.cleaned_data.get('purchases')
            if purchases_to_delete:
                Purchase.objects.filter(pk__in=purchases_to_delete).delete()
        return redirect('purchase-delete')


class CardActivationView(View):
    def get(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        card.status = 'activated'  #
        card.save()
        return redirect('card-list')

class CardDeactivationView(View):
    def get(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        card.status = 'deactivated'
        card.save()
        return redirect('card-list')

class CardDeleteView(View):
    def get(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        return render(request, 'card/card_delete_confirm.html', {'card': card})

class CardDeleteConfirmedView(View):
    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        card.delete()
        return redirect('card-list')


class CardListAPIView(generics.ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Card.objects.all()
        return queryset

class PurchaseListAPIView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Purchase.objects.all()
        return queryset


def purchase_filter(request):
    # Получите параметры фильтрации из запроса
    purchase_date = request.GET.get('purchase_date')
    card_number = request.GET.get('card_number')

    # Фильтруйте записи покупок на основе параметров фильтрации
    purchases = Purchase.objects.all()

    if purchase_date:
        purchases = purchases.filter(purchase_date=purchase_date)

    if card_number:
        purchases = purchases.filter(card__card_number=card_number)

    return render(request, 'card/purchase_filter.html', {'purchases': purchases})

class CardListView(ListView):
    model = Card
    template_name = 'card/card_list.html'  #
    context_object_name = 'cards'

    def get_queryset(self):
        form = CardSearchForm(self.request.GET)
        queryset = Card.objects.all()

        if form.is_valid():
            owner_name = form.cleaned_data.get('owner_name')
            card_number = form.cleaned_data.get('card_number')
            status = form.cleaned_data.get('status')

            if owner_name:
                queryset = queryset.filter(owner_name__icontains=owner_name)
            if card_number:
                queryset = queryset.filter(card_number__icontains=card_number)
            if status:
                queryset = queryset.filter(status__icontains=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CardSearchForm(self.request.GET)
        return context


class HomeView(View):
    def get(self, request):
        context = {
            'message': 'Добро пожаловать на главную страницу!',
        }
        return render(request,'home.html', context)
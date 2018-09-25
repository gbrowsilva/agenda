
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Comment
from django.utils.timezone import localdate
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse
from django.views.defaults import bad_request, server_error
from datetime import datetime, timedelta
from .models import Event, Comment
from .forms import EventForm, CommentForm


ITEMS_PER_PAGE = 5

def split_date(string_date):
    """Transformar a data em yyyy-mm-dd em uma tupla de tres valores para 
    utilizar na visão de eventos de um determinado dia."""
    for value in string_date.splint('-'):
        yield int(value)

# Create your views here.
def index(request):
    """ Exibe a página principal da aplicação."""
    context= {
        'hide_new_button': True,
        'priorities': Event.priorities_list,
        'today': localdate(),
    }
    return render(request, 'index.html', context)

""" Exibe todos os eventos em uma unica página, recebe o número da página a ser visualizada via GET. """
def all(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Event.objects.all(), ITEMS_PER_PAGE)
    total = paginator.count

    try:
        events = paginator.page(page)
    except InvalidPage:
        events = paginator.page(1)

    context = {
        'events': events,
        'total': total,
        'priorities': Event.priorities_list,
        'today': localdate(),
    }

    return render(request,'events.html', context)

""" Visualização dos eventos de um determinado dia, recebe a data em formato ano/mes/dia como parâmetro. """
def day(request, year: int, month: int, day: int):
    day = datetime(year, month, day)
    events = Event.objects.filter(date='{:%Y-%m-%d}'.format(day)).order_by('-priority', 'event')
    context = {
        'today': localdate(),
        'day': day,
        'events': events,
        'next': day + timedelta(days=1),
        'previous': day - timedelta(days=1),
        'priorities': Event.priorities_list,
    }

    return render(request, 'day.html', context)

def delete(request, id: int):
    """Apaga um evento especifico, se o evento nao existir resultará em erro 404, se algo errado ocorrer 
    retornara a pagina de erro"""
    event = get_object_or_404(Event, id=id)
    (year, month, day) = tuple(
        split_date('{:%y-%m-%d}'.format(event.date)))
    if event.delete():
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return server_error(request, 'ops_500.html')


def edit(request):
    """Edita o conteúdo de um evento, recebendo os dados enviados pelo formulário, 
    validando e populando en um evento já existente"""
    form = EventForm(request.POST)
    if form.is_valid():
        event = get_object_or_404(Event, id=request.POST['id'])
        event.date = form.cleaned_data['date']
        event.event = form.cleaned_data['event']
        event.priority = form.cleaned_data['priority']
        event.save()
        (year, month, day)= tuple(
            split_date('{:%y-%m-%d}'.format(event.date)))
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return bad_request(request, None, 'ops_400.html')

def new(request):
    """Recebendo os dados de um novo evento via post, faz a validação dos dados e aí insere na base de dados"""
    form = EventForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        #uso a data enviando pelo formulario para o redirecionamento.
        (year, month, day)= tuple(
            split_date(request.POST['date']))
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return bad_request(request, None, 'ops_400.html')

def show(request, id: int):

    """visualização de um determinado evento"""
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('agenda-events-show', id=id)
    context = {
        'events': event,
        'comments': Comment.objects.filter(event=id).order_by('-commented'),
        'hide_new_button': True,
        'priorities': Event.priorities_list,
        'today': localdate(),
    }
    return render(request, 'show.html', context)


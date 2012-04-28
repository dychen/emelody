import datetime

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('dateapp/current_datetime.html', {'current_date': current_date})

def hours_ahead(request, offset):
    try:
        hour_offset = int(offset)
    except ValueError:
        raise Http404()
    next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
    return render_to_response('dateapp/hours_ahead.html', locals())

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['subject'], cd['message'], cd.get('email', 'noreply@example.com'), ['siteowner@example.com'],)
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('contact_form.html', {'form': form})
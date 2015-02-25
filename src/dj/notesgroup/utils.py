# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from globals import MAILADMIN
from lxml.html.diff import htmldiff

def user_email(u):
    return u'"%s %s" <%s>' % (u.first_name, u.last_name, u.email)

def send_mail(sender, recipients, subject, body):
    """
    Tous les envois de mail doivent passer par cette methode
    > Pour l'instant non !!! (grep send_mail views.py)
    """
    if not recipients:
        return
    if sender:
        reply_to = user_email(sender)
        from_email = u'"%s %s" <%s>' % (sender.first_name, sender.last_name, MAILADMIN)
    else:
        from_email = reply_to = MAILADMIN
    recipients = [ user_email(u) for u in recipients ]
    msg = EmailMultiAlternatives(u'[NotesGroup] ' + subject,
                                 'notification notesgroup', 
                                 from_email, 
                                 recipients,
                                 headers = {'Reply-To': reply_to})
    msg.attach_alternative(body, "text/html")
    msg.send()


def note_diff(note1, note2):
    context = { 'note': note1, 
                'last_note' : note2,
                'note_src': note2.uid, 
                'http_root':settings.HTTP_ROOT }
    r1 = render_to_string('notesgroup/note_view.html', context)
    context['note'] = note2
    r2 = render_to_string('notesgroup/note_view.html', context)
    try:
        content = htmldiff(r1, r2)
    except KeyError:
        content = r2
    content = content.replace('class="group"', 'style="border:1px solid #CCCCCC; margin:1em 0 0; padding:0 1em;"')
    return content



def _set_paths(parent, reset):
    from models import Note
    try:
        for note in Note.objects.filter(parent=parent):
            if reset or not note.path:
                note.path = parent.path + '/%s' % note.uid
                note.save()
            _set_paths(note, reset)
    except UnicodeDecodeError:
        print "pb avec %s" % parent.uid

def set_paths(reset=True):
    from models import Note
    for note in Note.objects.filter(parent=0).exclude(uid=0):
        if reset or not note.path:
            note.path = '/%s' % note.uid
            note.save()
        _set_paths(note, reset)

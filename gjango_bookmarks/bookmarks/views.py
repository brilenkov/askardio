'''
from django.http import HttpResponse
def main_page(request):
  output = ur'
    <html>
      <head><title>%s</title></head>
      <body>
        <h1>%s</h1><p>%s</p>
      </body>
    </html>
  ' % (
    u'Django Bookmarks',
    u'Welcome to Django Bookmarks',
    u'Where you can store and share bookmarks!'
  )
  return HttpResponse(output)
'''
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
def main_page(request):
  return render_to_response(
  #  'main_page.html',
  'main_page.html', RequestContext(request)
  #  {'user': request.user} 
  )
  
  
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/register/success/')
  
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
def user_page(request, username):
  user = get_object_or_404(User, username=username)
  bookmarks = user.bookmark_set.order_by('-id')
  #try:
  #  user = User.objects.get(username=username)
  #except User.DoesNotExist:
  #  raise Http404(u'Requested user not found.')
  #bookmarks = user.bookmark_set.all()
  template = get_template('user_page.html')
  variables = RequestContext(request, {
    'username': username,
    'bookmarks': bookmarks,
    'show_tags': True
  })
  output = template.render(variables)
  #return HttpResponse(output)
  return render_to_response('user_page.html', variables)
  
from bookmarks.forms import *
def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/register/success/')
  else:
    form = RegistrationForm()
  
  variables = RequestContext(request, { 
     'form': form 
  })
  return render_to_response( 
    'registration/register.html',  
    variables 
  )
  
from bookmarks.models import *
from django.contrib.auth.decorators import login_required
@login_required
def bookmark_save_page(request):
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
      # Create or get link.
      link, dummy = Link.objects.get_or_create(
        url=form.cleaned_data['url']
      )
      # Create or get bookmark.
      bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        link=link
      )
      # Update bookmark title.
      bookmark.title = form.cleaned_data['title']
      # If the bookmark is being updated, clear old tag list.
      if not created:
        bookmark.tag_set.clear()
        # Create new tag list.
      tag_names = form.cleaned_data['tags'].split()
      for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)
      # Save bookmark to database.
      bookmark.save()
      return HttpResponseRedirect(
        '/user/%s/' % request.user.username
      )
  else:
    form = BookmarkSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('bookmark_save.html', variables)
  
def tag_page(request, tag_name):
  tag = get_object_or_404(Tag, name=tag_name)
  bookmarks = tag.bookmarks.order_by('-id')
  variables = RequestContext(request, {
    'bookmarks': bookmarks,
    'tag_name': tag_name,
    'show_tags': True,
    'show_user': True
  })
  return render_to_response('tag_page.html', variables)
  
def tag_cloud_page(request):
  MAX_WEIGHT = 5
  tags = Tag.objects.order_by('name')
  # Calculate tag, min and max counts.
  min_count = max_count = tags[0].bookmarks.count()
  for tag in tags:
    tag.count = tag.bookmarks.count()
    if tag.count < min_count:
      min_count = tag.count
    if max_count < tag.count:
      max_count = tag.count
  # Calculate count range. Avoid dividing by zero.
  range = float(max_count - min_count)
  if range == 0.0:
    range = 1.0
  # Calculate tag weights.
  for tag in tags:
    tag.weight = int(
      MAX_WEIGHT * (tag.count - min_count) / range
    )
  variables = RequestContext(request, {
    'tags': tags
  })
  return render_to_response('tag_cloud_page.html', variables)
  
def search_page(request):
  form = SearchForm()
  bookmarks = []
  show_results = False
  if 'query' in request.GET:
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      bookmarks = Bookmark.objects.filter(
        title__icontains=query
      )[:10]
  variables = RequestContext(request, {
    'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })
  return render_to_response('search.html', variables)
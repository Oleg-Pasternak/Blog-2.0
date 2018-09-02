from django.core.paginator import Paginator, EmptyPage,\
									PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.urls import reverse_lazy

class PostDetailView(FormView):
	template_name = 'blog/post/detail.html'
	form_class = CommentForm
	success_url = '.'

	def get(self,request, pk):
		# get post from database using pk (object identifier)
		post = get_object_or_404(Post, pk=pk)
		# get all active comments connected to post
		comments = Comment.objects.filter(post=post, active=True)
		# set form into variable and send into template
		form = CommentForm()
		# standart render function
		return render(request, 'blog/post/detail.html',
								{'comments': comments,
								'post':post,'form':form})

	def form_valid(self, form, **kwargs):
		# create new comment, but prevent saving it into database
		new_comment = form.save(commit=False)
		# get pk from url
		pk = self.kwargs['pk']
		# get post using pk
		post = get_object_or_404(Post, pk=pk)
		# connect comment with post
		new_comment.post = post
		# save comment into database
		new_comment.save()
		# Magic.
		return super(PostDetailView, self).form_valid(form)



class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3	
	template_name = 'blog/post/list.html'

class ErrorJsView(TemplateView):
	template_name = 'blog/noscript/noscript.html'

# class PostShaveView(FormView):
# 	form_class = EmailPostForm
#     success_url = ''
#
# 	def post(self, request, **kwargs):
# 		post_id = self.kwargs.get('post_id')
# 		if post_id:
# 			post = get_object_or_404(Post, id=post_id, status='published')


def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	if request.method == 'POST':
		# Form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			# ... send email
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post,
												'form': form})

#PageError
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

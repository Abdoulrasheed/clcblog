from django.shortcuts import render, redirect
from .models import Blog, Comment

def homepage(request):
	# select * from blog;
	blogs = Blog.objects.all()
	return render(request, 'blog/home.html', {"ourblogs": blogs})


def detail_post(request, blog_id):
	template = 'blog/detail_blog.html'
	# select * from blog where id=1
	blog = Blog.objects.get(id=blog_id)

	comments = blog.comment_set.all()

	context = {"blog": blog, "comments": comments}
	return render(request, template, context)


def post_comment(request):
	if request.method == "POST":
		data = request.POST
		name = data.get('person')
		comment = data.get('body')
		post = data.get('post')

		blog = Blog.objects.get(id=post)

		Comment.objects.create(
			commenter = name,
			comment = comment,
			post = blog
		).save()

	return redirect('homepage')

def like_post(request):
	from django.http import HttpResponse

	post = request.GET.get('post_id')
	action = int(request.GET.get('action'))

	blog = Blog.objects.get(id=post)

	l = blog.likes

	if action:
		blog.likes = l + 1
	else:
		blog.likes = l - 1

	blog.save()

	return HttpResponse(blog.likes)

	
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer
# import for pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# filtering 
from rest_framework.filters import SearchFilter, OrderingFilter


SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
@permission_classes((IsAuthenticated,)) #user have the token can only have the access
def api_detail_blog_view(request, slug):

	try:
		# BlogPost is a model
		blog_post = BlogPost.objects.get(slug=slug)

	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	

	if request.method == 'GET':
		#passing blog_post object got from database
		serializer = BlogPostSerializer(blog_post)
		# Returning serilized data from that serilizer
		return Response(serializer.data)


# @api_view(['PUT',])
# @permission_classes((IsAuthenticated,))
# def api_update_blog_view(request, slug):

# 	try:
# 		blog_post = BlogPost.objects.get(slug=slug)

# 	except BlogPost.DoesNotExist:
# 		return Response(status=status.HTTP_404_NOT_FOUND)


# 	# author is sam eone who is created this post to edit that post,,have access to user object throught the token (request.user)
# 	user = request.user
# 	if blog_post.author != user:
# 		return Response({'response': "You don't have permission to edit that!!!!!"})

# 	if request.method == 'PUT':
# 		serializer = BlogPostSerializer(blog_post, data=request.data)
# 		# data variable
# 		data = {}

# 		if serializer.is_valid():
# 			serializer.save()
# 			data[SUCCESS] = UPDATE_SUCCESS
# 			return Response(data=data)

# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = blog_post.pk
			data['title'] = blog_post.title
			data['body'] = blog_post.body
			data['slug'] = blog_post.slug
			data['date_updated'] = blog_post.date_updated
			#remove signature its not imp
			image_url = str(request.build_absolute_uri(blog_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['username'] = blog_post.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	# author is sam eone who is created this post to edit that post,,have access to user object throught the token (request.user)
	user = request.user
	if blog_post.author != user:
		return Response({'response': "You don't have permission to DELETE that!!!!!"})

	if request.method == 'DELETE':
		operation = blog_post.delete()
		data = {}
		# if operation 
		if operation:
			data[SUCCESS] = DELETE_SUCCESS
		else:
			data["failure"]="delete failed"

		return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):
	#get the one of account user who as the primary key = 1
	# account = Account.objects.get(pk=3)

	# get the account for the author ,with out author we don't create blogpost
	account = request.user
	blog_post = BlogPost(author=account)

	if request.method == 'POST':
		# passing blog post that already has author attach to it to the serializer
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBlogListView(ListAPIView):
	# query all those blog post pass it throught the context to the view
	class Meta:
		ordering = ['-id']
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backend =(SearchFilter,OrderingFilter)
	search_fields=('title','body','author__username')#author is the model __ to specify a perticual author model




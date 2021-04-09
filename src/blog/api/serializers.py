from rest_framework import serializers

from blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField('get_username_from_author')
	class Meta:
		model = BlogPost
		fields = ['pk','slug','title', 'body', 'image','date_updated','username']
    
	# create a new field usernname and that to fileds section in meta class overrrite section and serializermethod field and create a method
	# that responsible for returning the username
	def get_username_from_author(self,blog_post):
		username = blog_post.author.username
		return username




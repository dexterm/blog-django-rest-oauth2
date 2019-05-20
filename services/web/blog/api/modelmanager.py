from django.db import models
###
#  Querymanager for table Post
###
class PostManager(models.Manager):
    ###
    # for regular queries filter only approved posts
    ###
    def get_queryset(self):
        return super().get_queryset().filter(pstatus="AP")

    def all_objects(self):
        return super().get_queryset()

    def status(self, status_str= 'AP'):
        return self.all_objects().filter(pstatus=status_str)

###
#  Querymanager for table Category
###
class CategoryManager(models.Manager):
    ###
    # for regular queries filter only approved categories
    ###
    def get_queryset(self):
        return super().get_queryset().filter()

    def all_objects(self):
        return super().get_queryset()

###
#  Querymanager for table Category
###
class CommentManager(models.Manager):
    ###
    # for regular queries filter only approved categories
    ###
    def get_queryset(self):
        return super().get_queryset().filter(cstatus="AP")

    def all_objects(self):
        return super().get_queryset()
    ##
    #  default status = approved
    ##
    def status(self, status_str= 'AP'):
        return self.all_objects().filter(cstatus=status_str)

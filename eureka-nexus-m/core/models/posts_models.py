from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
import os


# a function to get a unique path for a profile picture
def get_unique_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_pictures', filename)


# a function to get a unique path for a post image
def get_unique_post_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('post_images', filename)


# a function to get a unique path for a post multimedia
def get_unique_multimedia_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('post_multimedia', filename)



# a model to store posts with the following fields:
# author: the user who created the post
# brand: the brand of the post
# colour: the colour of the post
# custom_colour: the custom colour of the post
# condition: the condition of the post
# custom_condition: the custom condition of the post    
# created_at: the date and time when the post was created
# depth: the depth of the post
# description: the description of the post
# elasticity: the elasticity of the post
# custom_elasticity: the custom elasticity of the post
# functionality: the functionality of the post
# custom_functionality: the custom functionality of the post
# hardness: the hardness of the post
# custom_hardness: the custom hardness of the post
# image: the image of the post
# image_description: the description of the image of the post
# icon: the icon of the post
# icon_description: the description of the icon of the post
# location: the location of the post
# markings: the markings of the post
# material: the material of the post
# custom_material: the custom material of the post
# other_multimedia: the other multimedia of the post
# origin: the origin of the post
# origin_of_acquisition: the origin of acquisition of the post
# pattern: the pattern of the post
# custom_pattern: the custom pattern of the post
# post: the post
# print_description: the description of the print of the post
# shape: the shape of the post
# custom_shape: the custom shape of the post
# size: the size of the post
# size_exactness: the exactness of the size
# size_type: the type of the size (exact, approximate)
# size_unit: the unit of the size
# approximate_size: the approximate size of the post
# height: the height of the post
# width: the width of the post
# length: the length of the post
# smell: the smell of the post
# custom_smell: the custom smell of the post
# status: the status of the post (unknown, solved)  
# taste: the taste of the post
# custom_taste: the custom taste of the post
# texture: the texture of the post
# custom_texture: the custom texture of the post
# time_period: the time period of the post
# custom_time_period: the custom time period of the post
# transparency: the transparency of the post
# custom_transparency: the custom transparency of the post  
# weight: the weight of the post
# weight_exactness: the exactness of the weight (exact, approximate)
# weight_type: the type of the weight (exact, approximate)
# weight_unit: the unit of the weight
# approximate_weight: the approximate weight of the post
# custom_approximate_weight: the custom approximate weight of the post
# exact_weight: the exact weight of the post
# updated_at: the date and time when the post was last updated 
# the relationship is one to many between post and comment and one post can have multiple comments and one comment can have only one post
# the relationship is one to many between post and multimedia and one post can have multiple multimedia and one multimedia can have only one post
# the relationship is one to many between post and wikidata_tag and one post can have multiple wikidata_tags and one wikidata_tag can have only one post
# the relationship is one to many between post and post_attribute and one post can have multiple post_attributes and one post_attribute can have only one post
# the relationship is one to many between post and post_multimedia and one post can have multiple post_multimedia and one post_multimedia can have only one post
class Post(models.Model):
    EXACTNESS_CHOICES = [
        ('exact', 'Exact'),
        ('approximate', 'Approximate'),
    ]
    
    COLOUR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('black', 'Black'),
        ('white', 'White'),
        ('brown', 'Brown'),
        ('grey', 'Grey'),
        ('other', 'Other'),
    ]
    
    SHAPE_CHOICES = [
        ('round', 'Round'),
        ('square', 'Square'),
        ('rectangular', 'Rectangular'),
        ('triangular', 'Triangular'),
        ('oval', 'Oval'),
        ('irregular', 'Irregular'),
        ('other', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('unknown', 'Unknown'),
        ('solved', 'Solved'),
    ]

    MATERIAL_CHOICES = [
        ('metal', 'Metal'),
        ('wood', 'Wood'),
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('fabric', 'Fabric'),
        ('ceramic', 'Ceramic'),
        ('other', 'Other'),
    ]

    TIME_PERIOD_CHOICES = [
        ('ancient', 'Ancient'),
        ('medieval', 'Medieval'),
        ('modern', 'Modern'),
        ('contemporary', 'Contemporary'),
        ('other', 'Other'),
    ]

    OBJECT_DOMAIN_CHOICES = [
        ('art_design', 'Art and Design'),
        ('technology', 'Technology'),
        ('household', 'Household'),
        ('fashion_accessories', 'Fashion and Accessories'),
        ('tools_equipment', 'Tools and Equipment'),
        ('toys_games', 'Toys and Games'),
        ('historical_cultural', 'Historical and Cultural'),
        ('other', 'Other'),
    ]

    HARDNESS_CHOICES = [
        ('soft', 'Soft'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('other', 'Other'),
    ]

    ELASTICITY_CHOICES = [
        ('elastic', 'Elastic'),
        ('non_elastic', 'Non-elastic'),
        ('semi_elastic', 'Semi-elastic'),
        ('other', 'Other'),
    ]

    TRANSPARENCY_CHOICES = [
        ('transparent', 'Transparent'),
        ('translucent', 'Translucent'),
        ('opaque', 'Opaque'),
        ('other', 'Other'),
    ]

    TEXTURE_CHOICES = [
        ('smooth', 'Smooth'),
        ('rough', 'Rough'),
        ('grainy', 'Grainy'),
        ('polished', 'Polished'),
        ('matte', 'Matte'),
        ('other', 'Other'),
    ]
    
    PATTERN_CHOICES = [
        ('plain', 'Plain'),
        ('patterned', 'Patterned'),
        ('striped', 'Striped'),
        ('checkered', 'Checkered'),
        ('marbled', 'Marbled'),
        ('other', 'Other'),
    ]
    
    TASTE_CHOICES = [
        ('sweet', 'Sweet'),
        ('salty', 'Salty'),
        ('metallic', 'Metallic'),
        ('bitter', 'Bitter'),
        ('sour', 'Sour'),
        ('other', 'Other'),
    ]
    
    SMELL_CHOICES = [
        ('odorless', 'Odorless'),
        ('chemical', 'Chemical'),
        ('earthy', 'Earthy'),
        ('metallic', 'Metallic'),
        ('fragrant', 'Fragrant'),
        ('other', 'Other'),
    ]
    
    FUNCTIONALITY_CHOICES = [
        ('rigid', 'Rigid'),
        ('moving', 'Moving'),
        ('adhesive', 'Adhesive'),
        ('other', 'Other'),
    ]
    
    WEIGHT_UNIT_CHOICES = [
        ('mg', 'Milligram'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('t', 'Ton'),
        ('oz', 'Ounce'),
        ('lb', 'Pound'),
        ('st', 'Stone'),
    ]
    
    APPROXIMATE_WEIGHT_CHOICES = [
        ('lightweight', 'Lightweight'),
        ('medium', 'Medium Weight'),
        ('heavy', 'Heavy'),
        ('other', 'Other'),
    ]
    
    SIZE_UNIT_CHOICES = [
        ('mm', 'Millimeter'),
        ('cm', 'Centimeter'),
        ('m', 'Meter'),
        ('km', 'Kilometer'),
        ('in', 'Inch'),
        ('ft', 'Foot'),
        ('yd', 'Yard'),
        ('mi', 'Mile'),
    ]

    LOCATION_CHOICES = [
        ('manual', 'Manual Input'),
        ('current', 'Current Location'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    # required fields
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to=get_unique_post_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional fields
    size = models.CharField(max_length=50, blank=True, null=True)
    size_exactness = models.CharField(max_length=20, choices=EXACTNESS_CHOICES, blank=True, null=True)
    size_type = models.CharField(max_length=20, choices=EXACTNESS_CHOICES, blank=True, null=True)
    approximate_size = models.CharField(max_length=100, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    size_unit = models.CharField(max_length=5, choices=SIZE_UNIT_CHOICES, blank=True, null=True)

    weight_type = models.CharField(max_length=20, choices=EXACTNESS_CHOICES, blank=True, null=True)
    approximate_weight = models.CharField(max_length=20, choices=APPROXIMATE_WEIGHT_CHOICES, blank=True, null=True)
    custom_approximate_weight = models.CharField(max_length=100, blank=True, null=True)
    exact_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=5, choices=WEIGHT_UNIT_CHOICES, blank=True, null=True)

    colour = models.CharField(max_length=20, choices=COLOUR_CHOICES, blank=True, null=True)
    custom_colour = models.CharField(max_length=50, blank=True, null=True)
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, blank=True, null=True)
    custom_shape = models.CharField(max_length=300, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    weight_exactness = models.CharField(max_length=20, choices=EXACTNESS_CHOICES, blank=True, null=True)
    texture = models.CharField(max_length=20, choices=TEXTURE_CHOICES, blank=True, null=True)
    custom_texture = models.CharField(max_length=300, blank=True, null=True)
    origin = models.CharField(max_length=300, blank=True, null=True)
    value = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    custom_condition = models.CharField(max_length=100, blank=True, null=True)
    smell = models.CharField(max_length=20, choices=SMELL_CHOICES, blank=True, null=True)
    custom_smell = models.CharField(max_length=300, blank=True, null=True)
    taste = models.CharField(max_length=20, choices=TASTE_CHOICES, blank=True, null=True)
    custom_taste = models.CharField(max_length=300, blank=True, null=True)
    origin_of_acquisition = models.CharField(max_length=300, blank=True, null=True)
    pattern = models.CharField(max_length=20, choices=PATTERN_CHOICES, blank=True, null=True)
    custom_pattern = models.CharField(max_length=300, blank=True, null=True)
    functionality = models.CharField(max_length=20, choices=FUNCTIONALITY_CHOICES, blank=True, null=True)
    custom_functionality = models.CharField(max_length=300, blank=True, null=True)
    other_multimedia = models.ImageField(upload_to='post_other_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, blank=True, null=True)
    custom_material = models.CharField(max_length=100, blank=True, null=True)
    image_description = models.TextField(max_length=500, blank=True, null=True)
    icon_description = models.TextField(max_length=500, blank=True, null=True)
    markings = models.TextField(max_length=500, blank=True, null=True)
    print_description = models.TextField(max_length=500, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    time_period = models.CharField(max_length=20, choices=TIME_PERIOD_CHOICES, blank=True, null=True)
    custom_time_period = models.CharField(max_length=100, blank=True, null=True)
    object_domain = models.CharField(max_length=30, choices=OBJECT_DOMAIN_CHOICES, blank=True, null=True)
    custom_object_domain = models.CharField(max_length=100, blank=True, null=True)
    hardness = models.CharField(max_length=20, choices=HARDNESS_CHOICES, blank=True, null=True)
    custom_hardness = models.CharField(max_length=100, blank=True, null=True)
    elasticity = models.CharField(max_length=20, choices=ELASTICITY_CHOICES, blank=True, null=True)
    custom_elasticity = models.CharField(max_length=100, blank=True, null=True)
    transparency = models.CharField(max_length=20, choices=TRANSPARENCY_CHOICES, blank=True, null=True)
    custom_transparency = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

    def has_answer_comment(self): # to check if the post has at least one comment marked as answer
        return self.comments.filter(tag='answer').exists()

    def upvote_count(self):
        return self.votes.filter(vote_type='up').count()
    
    def downvote_count(self):
        return self.votes.filter(vote_type='down').count()


# a model to store wikidata tags with the following fields:
# post: the post that the wikidata tag is associated with
# wikidata_id: the wikidata id of the tag
# label: the label of the tag
# link: the link to the wikidata page of the tag
# the relationship is one to many between post and wikidata_tag and one post can have multiple wikidata_tags and one wikidata_tag can have only one post # consider changing to many to many
class WikidataTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='wikidata_tags')
    wikidata_id = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    link = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({self.wikidata_id})"

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = f"https://www.wikidata.org/wiki/{self.wikidata_id}"
        super().save(*args, **kwargs)


# a model to store post attributes with the following fields:
# post: the post that the attribute is associated with
# name: the name of the attribute
# value: the value of the attribute
# instance_id: the instance id of the attribute
# created_at: the date and time when the attribute was created
# the relationship is one to many between post and post_attribute and one post can have multiple post_attributes and one post_attribute can have only one post
class PostAttribute(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    value = models.TextField()
    instance_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', 'instance_id']


# a model to store post multimedia with the following fields:
# post: the post that the multimedia is associated with
# file: the file of the multimedia
# file_type: the type of the file (image, video, audio, document)
# title: the title of the file
# description: the description of the file
# uploaded_at: the date and time when the file was uploaded
# order: the order of the file in the post
# the relationship is one to many between post and post_multimedia and one post can have multiple post_multimedia and one post_multimedia can have only one post
class PostMultimedia(models.Model):
    MULTIMEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='multimedia_files')
    file = models.FileField(upload_to=get_unique_multimedia_path)
    file_type = models.CharField(max_length=20, choices=MULTIMEDIA_TYPES)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"{self.get_file_type_display()} for {self.post.title}"

    def get_file_extension(self):
        return self.file.name.split('.')[-1].lower()

    def is_image(self):
        return self.get_file_extension() in ['jpg', 'jpeg', 'png', 'gif', 'webp']

    def is_video(self):
        return self.get_file_extension() in ['mp4', 'webm', 'ogg']

    def is_audio(self):
        return self.get_file_extension() in ['mp3', 'wav', 'ogg']

    def is_document(self):
        return self.get_file_extension() in ['pdf', 'doc', 'docx', 'txt']

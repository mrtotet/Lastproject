from .models import Recommend,Recommend_Category

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Recommend)
class ProjectTranslationOptions(TranslationOptions):
    pass
    #fields = ('rating',)

@register(Recommend_Category)
class ProjectTranslationOptions(TranslationOptions):
    pass
    #fields = ('rating',)
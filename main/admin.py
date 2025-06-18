

# Register your models here.
from django.contrib import admin
from .models import ChatHistory
from .models import Recommendation
from .models import LifeAdvice  

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'bot_response', 'sentiment', 'timestamp')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at',]
    readonly_fields = ['parameters', 'recommended_products', 'created_at']
    
@admin.register(LifeAdvice)
class LifeAdviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'advice', 'timestamp')
    readonly_fields = ('message', 'advice', 'timestamp')
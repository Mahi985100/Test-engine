from django.contrib import admin
from .models import Section, Question, TestAttempt, Answer
from django.utils.html import format_html
from django.urls import reverse

admin.site.register(Section)
admin.site.register(Question)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'score', 'is_marked', 'is_visited')
    can_delete = False

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'personality_type', 'completed', 'started_at', 'submitted_at', 'view_report_link')
    list_filter = ('completed', 'personality_type')
    search_fields = ('user__username', 'personality_type', 'career_matches')
    readonly_fields = ('started_at', 'submitted_at', 'total_score', 'analytical_score', 'leadership_score', 'communication_score', 'personality_type', 'career_matches', 'strengths', 'weaknesses')
    inlines = [AnswerInline]

    def view_report_link(self, obj):
        if obj.completed:
            url = reverse('report', args=[obj.id])
            return format_html('<a href="{}" target="_blank">Download/View Report</a>', url)
        return "-"
    view_report_link.short_description = 'Report'

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Avg
        extra_context = extra_context or {}
        extra_context['summary_stats'] = {
            'total_users': User.objects.count(),
            'total_questions': Question.objects.count(),
            'total_attempts': TestAttempt.objects.count(),
            'completed_tests': TestAttempt.objects.filter(completed=True).count(),
            'avg_score': TestAttempt.objects.filter(completed=True).aggregate(Avg('total_score'))['total_score__avg'] or 0,
        }
        return super().changelist_view(request, extra_context=extra_context)
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'completed', 'started_at', 'submitted_at')
        }),
        ('Scores', {
            'fields': ('total_score', 'analytical_score', 'leadership_score', 'communication_score')
        }),
        ('Analysis', {
            'fields': ('personality_type', 'career_matches', 'strengths', 'weaknesses')
        }),
    )

admin.site.register(Answer)

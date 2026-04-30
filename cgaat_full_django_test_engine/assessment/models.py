from django.db import models
from django.contrib.auth.models import User

class Section(models.Model):
    name = models.CharField(max_length=120)
    meaning = models.TextField()
    order = models.PositiveIntegerField(default=1)
    def __str__(self): return self.name

class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    score_a = models.IntegerField(default=1)
    option_b = models.CharField(max_length=255)
    score_b = models.IntegerField(default=2)
    option_c = models.CharField(max_length=255)
    score_c = models.IntegerField(default=3)
    option_d = models.CharField(max_length=255)
    score_d = models.IntegerField(default=4)
    order = models.PositiveIntegerField(default=1)
    skill_tag = models.CharField(max_length=80, default='General')
    def __str__(self): return self.text[:60]

class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    total_score = models.IntegerField(default=0)
    analytical_score = models.IntegerField(default=0)
    leadership_score = models.IntegerField(default=0)
    communication_score = models.IntegerField(default=0)
    personality_type = models.CharField(max_length=100, blank=True)
    career_matches = models.CharField(max_length=255, blank=True)
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    def __str__(self): return f'{self.user.username} - Attempt {self.id}'

class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)
    score = models.IntegerField(default=0)
    is_marked = models.BooleanField(default=False)
    is_visited = models.BooleanField(default=False)
    class Meta:
        unique_together = ('attempt','question')

from django.db import models
from django.contrib.auth import get_user_model
from src.apps.common.models import TimestampedModel

User = get_user_model()


class UserProgress(TimestampedModel):
    """Track user progress on questions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='user_progress')

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('partially_solved', 'Partially Solved'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    attempts = models.IntegerField(default=0)
    best_submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    points_earned = models.IntegerField(default=0)
    first_solved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title} - {self.status}"


class Achievement(TimestampedModel):
    """User achievements and badges"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#ffd700')

    # Achievement criteria
    required_problems_solved = models.IntegerField(null=True, blank=True)
    required_points = models.IntegerField(null=True, blank=True)
    required_streak = models.IntegerField(null=True, blank=True)
    required_category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class UserAchievement(TimestampedModel):
    """User's earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
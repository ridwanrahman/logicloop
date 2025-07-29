from django.db import models
from django.contrib.auth import get_user_model
from src.apps.common.models import TimestampedModel

User = get_user_model()


class Submission(TimestampedModel):
    """User submissions for questions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('time_limit_exceeded', 'Time Limit Exceeded'),
        ('memory_limit_exceeded', 'Memory Limit Exceeded'),
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('c', 'C'),
        ('javascript', 'JavaScript'),
        ('go', 'Go'),
        ('rust', 'Rust'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')

    # Execution details
    execution_time = models.FloatField(null=True, blank=True)  # in seconds
    memory_used = models.IntegerField(null=True, blank=True)  # in MB
    points_earned = models.IntegerField(default=0)

    # Results
    passed_test_cases = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.question.title} - {self.status}"

    @property
    def is_successful(self):
        return self.status == 'accepted'


class SubmissionResult(TimestampedModel):
    """Individual test case results for submissions"""
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='results')
    test_case = models.ForeignKey('questions.TestCase', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Submission.STATUS_CHOICES)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.submission} - Test Case {self.test_case.id} - {self.status}"

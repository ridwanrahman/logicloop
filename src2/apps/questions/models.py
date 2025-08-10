from django.db import models
from django.contrib.auth import get_user_model
from src2.apps.common.models import TimestampedModel

User = get_user_model()


class Difficulty(models.Model):
    """Difficulty levels for questions"""
    name = models.CharField(max_length=20, unique=True)  # Easy, Medium, Hard
    level = models.IntegerField(unique=True)  # 1, 2, 3
    color = models.CharField(max_length=7, default='#28a745')
    points = models.IntegerField(default=10)  # Points awarded for solving

    class Meta:
        ordering = ['level']
        verbose_name_plural = 'Difficulties'

    def __str__(self):
        return self.name


class Question(TimestampedModel):
    """Main question model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    problem_statement = models.TextField()
    input_format = models.TextField(blank=True)
    output_format = models.TextField(blank=True)
    constraints = models.TextField(blank=True)

    # Relationships
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('categories.Tag', related_name='questions', blank=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, related_name='questions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions')

    # Status and metrics
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    total_submissions = models.IntegerField(default=0)
    successful_submissions = models.IntegerField(default=0)

    # Additional fields
    hints = models.JSONField(default=list, blank=True)  # List of hints
    time_limit = models.IntegerField(default=5)  # seconds
    memory_limit = models.IntegerField(default=256)  # MB

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def success_rate(self):
        if self.total_submissions == 0:
            return 0
        return (self.successful_submissions / self.total_submissions) * 100


class TestCase(TimestampedModel):
    """Test cases for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)  # Sample test cases shown to users
    is_hidden = models.BooleanField(default=True)  # Hidden test cases for evaluation
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['is_sample', 'id']

    def __str__(self):
        return f"{self.question.title} - Test Case {self.id}"


class QuestionExample(TimestampedModel):
    """Examples to help users understand the question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='examples')
    input_example = models.TextField()
    output_example = models.TextField()
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

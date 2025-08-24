# Import your models here
from users.models import UserProfile, User
from categories.models import Category, Tag
from questions.models import Difficulty, Question, TestCase, QuestionExample
from submissions.models import Submission, SubmissionResult
from progress.models import UserProgress, Achievement, UserAchievement
from discussion.models import Discussion, DiscussionReply, Vote


def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing existing data...")

    # Clear in reverse dependency order
    # Vote.objects.all().delete()
    # DiscussionReply.objects.all().delete()
    # Discussion.objects.all().delete()
    # UserAchievement.objects.all().delete()
    # Achievement.objects.all().delete()
    # UserProgress.objects.all().delete()
    # SubmissionResult.objects.all().delete()
    # Submission.objects.all().delete()
    # TestCase.objects.all().delete()
    # QuestionExample.objects.all().delete()
    # Question.objects.all().delete()
    # Tag.objects.all().delete()
    # Category.objects.all().delete()
    # Difficulty.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.exclude(is_superuser=True).exclude(is_staff=True).delete()

    print("✅ Database cleared!")


clear_database()
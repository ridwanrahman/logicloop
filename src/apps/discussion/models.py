from django.db import models
from django.contrib.auth import get_user_model
from src.apps.common.models import TimestampedModel

User = get_user_model()


class Discussion(TimestampedModel):
    """Discussion threads for questions"""
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Status
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class DiscussionReply(TimestampedModel):
    """Replies to discussion threads"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_replies')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # Voting
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.author.username}"


class Vote(TimestampedModel):
    """User votes on discussion replies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(DiscussionReply, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(
        max_length=10,
        choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')]
    )

    class Meta:
        unique_together = ['user', 'reply']

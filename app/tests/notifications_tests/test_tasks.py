import pytest
from actstream.models import Action
from django.core import mail
from django.utils.timezone import now
from machina.apps.forum.models import Forum
from machina.apps.forum_conversation.models import Topic

from grandchallenge.notifications.models import Notification
from grandchallenge.notifications.tasks import send_unread_notification_emails
from tests.factories import UserFactory
from tests.notifications_tests.factories import (
    ForumFactory,
    NotificationFactory,
    TopicFactory,
)


@pytest.mark.django_db
def test_notification_email():
    user1 = UserFactory()
    user2 = UserFactory()
    f = ForumFactory(type=Forum.FORUM_POST)
    _ = TopicFactory(forum=f, poster=user2, type=Topic.TOPIC_POST)
    _ = NotificationFactory(user=user1, action=Action.objects.get())

    assert user1.user_profile.has_unread_notifications
    assert user1.user_profile.receive_notification_emails
    assert len(mail.outbox) == 0
    send_unread_notification_emails()
    assert len(mail.outbox) == 1
    email = mail.outbox[-1]
    assert email.to[0] == user1.email
    assert "You have 1 new notification" in email.body


@pytest.mark.django_db
def test_notification_email_last_sent_at_updated():
    user1 = UserFactory()
    user2 = UserFactory()
    f = ForumFactory(type=Forum.FORUM_POST)
    _ = TopicFactory(forum=f, poster=user2, type=Topic.TOPIC_POST)
    _ = NotificationFactory(user=user1, action=Action.objects.get())
    assert not user1.user_profile.notification_email_last_sent_at
    send_unread_notification_emails()
    user1.refresh_from_db()
    assert user1.user_profile.notification_email_last_sent_at


@pytest.mark.django_db
def test_notification_email_only_about_new_unread_notifications():
    user1 = UserFactory()
    user2 = UserFactory()
    f = ForumFactory(type=Forum.FORUM_POST)
    _ = TopicFactory(forum=f, poster=user2, type=Topic.TOPIC_POST)
    _ = NotificationFactory(user=user1, action=Action.objects.get())

    # mimic sending notification email by updating time stamp
    user1.user_profile.notification_email_last_sent_at = now()
    user1.user_profile.save()

    _ = NotificationFactory(user=user1, action=Action.objects.get())
    Notification.objects.all()
    send_unread_notification_emails()

    # user2 has 2 unread notifications
    assert len(user1.user_profile.unread_notifications) == 2
    # but only receives an email about unread notifications since the last email
    assert mail.outbox[-1].to[0] == user1.email
    assert "You have 1 new notification" in mail.outbox[-1].body


@pytest.mark.django_db
def test_notification_email_opt_out():
    user1 = UserFactory()
    user1.user_profile.receive_notification_emails = False
    user1.user_profile.save()

    user2 = UserFactory()
    f = ForumFactory(type=Forum.FORUM_POST)
    _ = TopicFactory(forum=f, poster=user2, type=Topic.TOPIC_POST)
    _ = NotificationFactory(user=user1, action=Action.objects.get())

    send_unread_notification_emails()
    assert len(mail.outbox) == 0

    user1.user_profile.receive_notification_emails = True
    user1.user_profile.save()

    send_unread_notification_emails()
    assert len(mail.outbox) == 1

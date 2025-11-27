from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Fee, Result
from students.models import Student

@shared_task
def send_fee_reminder(fee_id):
    """Send fee reminder to parent"""
    try:
        fee = Fee.objects.get(id=fee_id)
        parent = fee.student.parent
        
        if not parent.email:
            return f"No email for parent of {fee.student.full_name}"
        
        subject = f"Fee Reminder for {fee.student.full_name}"
        message = f"""
Dear {parent.get_full_name()},

This is a reminder about the pending fee for {fee.student.full_name}.

Fee Details:
- Amount: ${fee.amount}
- Amount Paid: ${fee.amount_paid}
- Balance Due: ${fee.balance}
- Due Date: {fee.due_date.strftime('%B %d, %Y')}

Please make the payment at your earliest convenience.

Thank you,
School Administration
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [parent.email],
            fail_silently=False,
        )
        
        return f"Reminder sent to {parent.email}"
    except Exception as e:
        return f"Error sending reminder: {str(e)}"


@shared_task
def send_fee_reminders():
    """Send reminders for fees due in next 7 days"""
    next_week = timezone.now().date() + timedelta(days=7)
    pending_fees = Fee.objects.filter(
        status__in=['PENDING', 'PARTIAL'],
        due_date__lte=next_week,
        due_date__gte=timezone.now().date()
    )
    
    count = 0
    for fee in pending_fees:
        send_fee_reminder.delay(fee.id)
        count += 1
    
    return f"Sent {count} fee reminders"


@shared_task
def send_overdue_fee_alerts():
    """Send alerts for overdue fees"""
    overdue_fees = Fee.objects.filter(
        status='OVERDUE',
        due_date__lt=timezone.now().date()
    )
    
    count = 0
    for fee in overdue_fees:
        parent = fee.student.parent
        if parent.email:
            subject = f"OVERDUE: Fee Payment for {fee.student.full_name}"
            message = f"""
Dear {parent.get_full_name()},

This is an urgent notice regarding the overdue fee for {fee.student.full_name}.

Fee Details:
- Amount: ${fee.amount}
- Amount Paid: ${fee.amount_paid}
- Balance Due: ${fee.balance}
- Due Date: {fee.due_date.strftime('%B %d, %Y')} (OVERDUE)

Please contact the school office immediately to arrange payment.

Thank you,
School Administration
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [parent.email],
                fail_silently=False,
            )
            count += 1
    
    return f"Sent {count} overdue alerts"


@shared_task
def send_result_notification(result_id):
    """Send notification when new result is added"""
    try:
        result = Result.objects.get(id=result_id)
        parent = result.student.parent
        
        if not parent.email:
            return f"No email for parent of {result.student.full_name}"
        
        subject = f"New Result Posted for {result.student.full_name}"
        message = f"""
Dear {parent.get_full_name()},

A new result has been posted for {result.student.full_name}.

Subject: {result.subject.name}
Term: {result.term}
Marks: {result.marks_obtained}/{result.total_marks}
Percentage: {result.percentage:.2f}%
Grade: {result.grade}

You can view the complete report card by logging into the parent portal.

Thank you,
School Administration
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [parent.email],
            fail_silently=False,
        )
        
        return f"Result notification sent to {parent.email}"
    except Exception as e:
        return f"Error sending notification: {str(e)}"


@shared_task
def send_bulk_announcement_email(announcement_id):
    """Send announcement via email to relevant users"""
    from announcements.models import Announcement
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        
        # Get recipients based on audience
        if announcement.audience == 'ALL':
            users = User.objects.filter(is_active=True).exclude(email='')
        elif announcement.audience == 'PARENTS':
            users = User.objects.filter(role='PARENT', is_active=True).exclude(email='')
        elif announcement.audience == 'TEACHERS':
            users = User.objects.filter(role='TEACHER', is_active=True, is_approved=True).exclude(email='')
        else:
            users = User.objects.none()
        
        emails = list(users.values_list('email', flat=True))
        
        if emails:
            subject = f"[{announcement.get_priority_display()}] {announcement.title}"
            message = f"""
{announcement.content}

---
Published: {announcement.publish_date.strftime('%B %d, %Y')}
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                emails,
                fail_silently=False,
            )
            
            return f"Announcement sent to {len(emails)} recipients"
        
        return "No recipients found"
    except Exception as e:
        return f"Error sending announcement: {str(e)}"
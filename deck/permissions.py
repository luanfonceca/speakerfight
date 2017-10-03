def has_manage_schedule_permission(user, event):
    if user.is_superuser:
        return True
    else:
        return event.user_in_jury(user)

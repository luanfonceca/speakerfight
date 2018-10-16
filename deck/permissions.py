def has_manage_schedule_permission(user, event):
    return user.is_superuser or event.user_in_jury(user)

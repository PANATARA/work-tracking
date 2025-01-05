from apps.users.models.users import User


def all_users_exists(users: list[User | int]) -> bool:
    """Validate that all users in the list exist."""
    if isinstance(users, (User, int)):
        users = [users]

    user_ids = [user.id if isinstance(user, User) else user for user in users]

    return all(User.objects.filter(pk=user_id).exists() for user_id in user_ids)

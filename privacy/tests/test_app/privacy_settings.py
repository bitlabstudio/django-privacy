"""Privacy settings for the ``test_app`` app."""


def get_clearance_level(owner, requester):
    """
    4 = self
    3 = friend
    2 = friend of friend
    1 = public

    """
    if owner == requester:
        return 4
    if requester.user in owner.friends.all():
        return 3

    # Get friends of friends
    owner_friends_pks = owner.friends.values_list('pk')
    requester_friends_pks = requester.friends.values_list('pk')
    if set(owner_friends_pks) & set(requester_friends_pks):
        return 2
    return 1

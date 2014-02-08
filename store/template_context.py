from store.utils import member_is_logged_in


def member_logged_in(request):
    return {
        'member_logged_in': member_is_logged_in(request),
    }

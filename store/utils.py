def member_is_logged_in(request):
    return request.session.get('member', False)


def log_member_in(request):
    request.session['member'] = True

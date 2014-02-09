def log_member_in(request):
    if not request.user.is_member:
        request.user.is_member = True
        request.user.save()

def log_member_in(request):
    if not request.user.voices_member:
        request.user.voices_member = True
        request.user.save()

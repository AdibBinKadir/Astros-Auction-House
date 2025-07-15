def is_mobile_or_tablet(request):
    """
    Returns True if the request is from a mobile or tablet device, based on the user-agent.
    """
    user_agent = str(request.META.get("HTTP_USER_AGENT", "")).lower()
    return any(device in user_agent for device in ["mobile", "tablet", "ipad"])


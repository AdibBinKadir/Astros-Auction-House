import pytz

def is_mobile_or_tablet(request):
    """
    Detects if the request was made from a mobile or tablet device.

    Args:
        request (HttpRequest): The incoming Django HTTP request object.

    Returns:
        bool: True if the request is from a mobile or tablet, False otherwise.
    """
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    return any(keyword in user_agent for keyword in ["mobile", "tablet", "ipad"])


def get_display_time(dt):
    """
    Converts a datetime object to a formatted 12-hour time with AM/PM.

    Args:
        dt (datetime): A timezone-aware datetime object.

    Returns:
        tuple: (hour as str, minute as str, period as str ["AM"/"PM"])
    """
    hour = dt.strftime("%H")
    minute = dt.strftime("%M")

    if int(hour) >= 12:
        period = "PM"
        hour = str(int(hour) - 12) if int(hour) > 12 else hour
    else:
        period = "AM"
        hour = "12" if int(hour) == 0 else hour

    return hour, minute, period



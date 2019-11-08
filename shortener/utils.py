from datetime import timedelta

def build_short_url(secure, host, shortid):
    short_url = ""
    if secure:
        short_url = f"https://{host}/{shortid}"
    else:
        short_url = f"http://{host}/{shortid}"

    return short_url

def build_day_count(queryset):
    total_visits = len(queryset)
    first_day = queryset.values()[0]
    last_day = queryset.values()[total_visits - 1]
    num_days = first_day['visit'] - last_day['visit']

    vpd = total_visits / abs(num_days.days)
    return vpd

def build_short_url(secure, host, shortid):
    short_url = ""
    if secure:
        short_url = f"https://{host}/{shortid}"
    else:
        short_url = f"http://{host}/{shortid}"

    return short_url
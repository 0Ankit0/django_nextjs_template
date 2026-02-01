from urllib.parse import urlencode


def _api_encode(data, prefix=None):
    """
    Encode nested dictionary for Stripe API requests.
    Compatible with Stripe 14.x which removed the internal _api_encode function.
    """
    encoded = []
    for key, value in data.items():
        if prefix:
            key = f"{prefix}[{key}]"
        if isinstance(value, dict):
            encoded.extend(_api_encode(value, key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    encoded.extend(_api_encode(item, f"{key}[{i}]"))
                else:
                    encoded.append((f"{key}[{i}]", item))
        else:
            encoded.append((key, value))
    return encoded


def stripe_encode(data):
    encoded_params = urlencode(list(_api_encode(data)))
    return encoded_params.replace("%5B", "[").replace("%5D", "]")

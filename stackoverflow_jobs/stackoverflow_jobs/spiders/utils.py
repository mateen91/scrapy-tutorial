import re


def clean(to_clean):
    if isinstance(to_clean, str):
        return re.sub('\s+', ' ', to_clean).strip()
    return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]
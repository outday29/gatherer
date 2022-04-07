def clean_name(filename):
    # Remove invalid Windows filename symbols
    filename = filename.strip()
    return filename.translate({ord(c):'' for c in ['>', '<', ':', '"', '/', '\\', '|', '?', '*', '\r', '\n']})
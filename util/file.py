def clean_name(filename):
    filename = filename.strip()
    return filename.translate({ord(c):'' for c in ['>', '<', ':', '"', '/', '\\', '|', '?', '*', '\r', '\n']})
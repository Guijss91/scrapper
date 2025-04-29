from urllib.parse import urlparse

def is_internal_link(base, link):
    """Verifica se o link é interno em relação à base"""
    base_domain = urlparse(base).netloc
    link_domain = urlparse(link).netloc
    return (link_domain == "" or link_domain == base_domain)

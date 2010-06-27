VALID_TAGS = ('p', 'em', 'strong', 'ul', 'ol', 'li', 'blockquote')

def purge_html(soup, valid_tags=None):
    from BeautifulSoup import Comment
    
    if valid_tags is None: valid_tags = VALID_TAGS
    
    # Remove comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    # Remove unwanted markup
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = []
    
    return soup

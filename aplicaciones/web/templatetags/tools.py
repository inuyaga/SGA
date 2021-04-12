from django import template
register = template.Library() 

@register.filter
def get_color_class_status_solicitud(status_num):
    color_status = ''
    if status_num == 1:        
        color_status ='text-orange'
    elif status_num == 2:        
        color_status = 'text-blue'
    elif status_num == 3:
        color_status = 'text-green'
    return color_status

@register.filter
def delete_page_url(url):   
    url = url.copy() 
    if 'page' in url:
        del url['page']
    url_decode = url.urlencode()    
    
        
    return url_decode
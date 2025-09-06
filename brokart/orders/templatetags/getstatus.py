from django import template

register=template.Library()

@register.simple_tag(name='getstatus')

def getstatus(status):
   status=status-1
   order_status=[ 'Confirmed','Processed','Delivered','Rejected']
   return order_status[status]
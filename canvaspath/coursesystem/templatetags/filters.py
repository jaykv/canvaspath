from django.template.defaulttags import register

@register.filter
def key(d, key_name):
	try:
		return d[key_name]
	except:
		return None
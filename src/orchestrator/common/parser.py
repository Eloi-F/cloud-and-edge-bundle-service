# URN format example :
# "urn:node:server"
URN_SEPARATOR = ":"

# URL format example :
# "http://server-ip:port/service"
URL_SEPARATOR = "/"

def parse_urn(field: str) -> str:
	"""Get payload from urn field in ODRL policies."""
	return field.rsplit(URN_SEPARATOR,1)[-1]

def parse_url(field: str, count: int = 1) -> str:
	"""Get payload from url field in ODRL policies."""
	return field.rsplit(URL_SEPARATOR,count)[-count]

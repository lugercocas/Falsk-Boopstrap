def es_flotante(variable):
	try:
		float(variable)
		return True
	except:
		return False
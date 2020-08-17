def search_for_pictures(search_term, store):
	pictures = store.get_all_pictures()

	def filter_function(picture):
		if search_term in picture.get('author', ''):
			return True
		if search_term in picture.get('camera', ''):
			return True
		if search_term in picture.get('tags', ''):
			return True
		return False

	return list(filter(filter_function, pictures))
def search_for_pictures(search_term, store):
	pictures = store.get_all_pictures()

	def filter_function(picture):
		if search_term in picture['author']:
			return True
		if search_term in picture['camera']:
			return True
		if search_term in picture['tags']:
			return True
		return False

	return list(filter(filter_function, pictures))
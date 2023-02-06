def parse_google_map_iframe(link):

	if link == None or link == "":
		return None

	if link.startswith("<iframe "):
			link = link[link.index('"')+1:]
			link = link[:link.index('"')]
			print(link)
			# google_map = google_map.replace('<iframe src="','')
			# google_map = google_map.replace('" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>','')

	if not link.startswith("https://www.google.com/maps/embed"):
		print("link is broken")
		raise ValidationError("iframe is broken")

	return link

def parse_google_map_link(link):
	if link == None or link == "":

		return None

	if not link.startswith("https://goo.gl/map"):
		print("link is broken")
		raise ValidationError("link is broken")

	return link
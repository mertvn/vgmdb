import bs4

from . import utils

def parse_event_page(html_source):
	event_info = {}
	html_source = utils.fix_invalid_table(html_source)
	soup = bs4.BeautifulSoup(html_source)
	soup_innermain = soup.find(id='innermain')
	soup_profile = soup_innermain.find_parent('div')
	soup_sections = soup_profile.find_all('div', recursive=False)
	soup_name_sections = soup_sections[0].find_all('span', recursive=False)

	event_info['name'] = soup_name_sections[1].string.strip()
	event_info['date'] = utils.parse_date_time(soup_name_sections[2].string.strip())

	notes = ''
	for soup_note in soup_sections[1].div.children:
		if isinstance(soup_note, bs4.Tag):
			notes += soup_note.string
		else:
			notes += unicode(soup_note)
	event_info['notes'] = notes.strip()

	event_info['releases'] = _parse_event_releases(soup_sections[2].table)

	return event_info

def _parse_event_releases(soup_table):
	releases = []
	if not soup_table:
		return releases

	soup_rows = soup_table.find_all('tr', recursive=False)
	if len(soup_rows) == 0:
		return releases

	for soup_row in soup_rows[1:]:
		release = {}
		soup_cells = soup_row.find_all('td', recursive=False)
		if len(soup_cells)<5:
			continue

		release['release_type'] = soup_cells[0].span.string
		release['catalog'] = soup_cells[1].span.string
		soup_class = soup_cells[1].span['class']
		if len(soup_class) == 2 and '-' in soup_class[1]:
			release['album_type'] = soup_class[1].split('-')[1]
		release['titles'] = utils.parse_names(soup_cells[3].a)
		release['link'] = soup_cells[3].a['href']
		release['release_date'] = utils.parse_date_time(soup_cells[5].span.string.strip())

		if soup_cells[4].a:
			release['publisher'] = {
				'link': soup_cells[4].a['href'],
				'names': utils.parse_names(soup_cells[4].a)}
		else:
			release['publisher'] = {
				'names': {"en": soup_cells[4].string.strip()}}
		releases.append(release)
	return releases


		


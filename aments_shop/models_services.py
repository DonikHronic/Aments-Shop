def convert_text(inner_text: str):
	"""
	Транслитерирует текст из русских символов в текст из английских символов
	:param inner_text: str
	:return: transliterated_text
	"""

	lower_case_letters = {
		u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'zh', u'з': u'z',
		u'и': u'i', u'й': u'y', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r',
		u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch',
		u'ъ': u'', u'ы': u'y', u'ь': u'', u'э': u'e', u'ю': u'yu', u'я': u'ya', u' ': u'_'
	}

	transliterated_text = ''
	for index, char in enumerate(str(inner_text).lower()):
		if char in lower_case_letters:
			transliterated_text += lower_case_letters[char]
		else:
			transliterated_text += char

	return transliterated_text


def image_path(instance, filename):
	return f'products/{convert_text(instance.product)}/{filename}'

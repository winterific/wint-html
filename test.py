from wint_html import *
from datetime import date

def layout(**kwargs):
	css = """
	body {
		color: blue;
	}
	"""
	return html5doctype + str(html(
        head(
            meta(name='charset', content='utf-8'),
            meta(name='viewport', content='width=device-width, initial-scale=1'),
            title('Test Page'),
            style(css, type='text/css')
        ),
        body(
			header(
				h1('Test Page')
			),
			main(kwargs.get('main', '')),
			footer(
				p(f'&copy; {date.today().year} Jean-Luc Picard')
			)
		)
    ))

page = layout(main='Hello world!')
print(page)

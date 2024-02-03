import scrapy


class SueldosSpider(scrapy.Spider):
    name = 'sueldos'
    start_urls = ['https://sueldode.org/']

    def parse(self, response):
        link_parties = response.css('a.no-lightbox::attr(href)').getall()
        for link in link_parties:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_party)

    def parse_party(self, response):
        nombre_personas = response.css('li a::attr(href)').getall()
        for referencia in nombre_personas:
            yield scrapy.Request(response.urljoin(referencia), callback=self.parse_politician)

    def parse_politician(self, response):
        nombre_vasallo = response.css('article[id] h1::text').get()
        puesto_vasallo = response.css('div.entry-content h2::text').get()
        salario_vasallo = response.css('p:contains("Salario bruto mensual")::text').get()
        anual_vasallo = response.css('p:contains("Salario bruto anual")::text').get()
        yield {
                'nombre': nombre_vasallo,
                'puesto': puesto_vasallo,
                'salario': salario_vasallo,
                'anual': anual_vasallo
            }
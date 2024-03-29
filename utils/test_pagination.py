from unittest import TestCase
from utils.pagination import make_pagination_range, make_pagination

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_for_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2,3,4,5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9,10,11,12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=14,
        )['pagination']
        self.assertEqual([13,14,15,16], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

    def test_value_error_for_current_page(self):
        # Definindo uma queryset vazia apenas para fins de teste
        queryset = []
        per_page = 10
        
        # Criando uma requisição falsa com um valor inválido para a página
        request = type('FakeRequest', (object,), {'GET': {'page': 'invalid'}})()
        
        # Chamando a função make_pagination com a requisição falsa
        page_obj, pagination_range = make_pagination(request, queryset, per_page)
        
        # Verificando se a página atual foi definida como 1 quando ValueError foi lançado
        assert page_obj.number == 1
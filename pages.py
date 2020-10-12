from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By

from transaction import Transaction


class FtPage(Page):
    def __init__(self, driver, base_url=None, timeout=40, **url_kwargs):
        super().__init__(driver, base_url, timeout, **url_kwargs)


class AutocompleteSuggestions(Region):

    _root_locator = (By.CSS_SELECTOR, "div.mod-ui-autocomplete__suggestions")

    @property
    def loaded(self):
        return bool(self.suggestions_elements)

    @property
    def suggestions_elements(self):
        return self.find_elements(
            By.CSS_SELECTOR, "div.mod-ui-autocomplete__suggestion"
        )

    def select_best_match(self):
        self.suggestions_elements[0].click()


class DatePicker(Region):

    _root_locator = (By.CSS_SELECTOR, "div.picker__holder")

    @property
    def year_element(self):
        return self.find_element(
            By.CSS_SELECTOR, "select.picker__select--year option[selected]"
        )

    @property
    def month_element(self):
        return self.find_element(By.CSS_SELECTOR, "div.picker__month")

    def previous_month(self):
        self.find_element(By.CSS_SELECTOR, "div.picker__nav--prev").click()

    @property
    def day_elements(self):
        return self.find_elements(By.CSS_SELECTOR, "div.picker__day--infocus")

    @property
    def date(self):
        raise NotImplementedError()

    @date.setter
    def date(self, value):
        year = value.strftime("%Y")
        month = value.strftime("%B")
        while self.year_element.text != year or self.month_element.text != month:
            self.previous_month()

        day = str(value.day)
        next(d for d in self.day_elements if d.text == day).click()


class AddTransactionForm(Region):

    _root_locator = (By.CSS_SELECTOR, "div.mod-portfolio-ui-overlays-add-transaction")

    def _input(self, name):
        return self.find_element(By.CSS_SELECTOR, f'input[name="{name}"]')

    @property
    def quantity(self):
        raise NotImplementedError()

    @quantity.setter
    def quantity(self, value):
        self._input("quantity").send_keys(str(value))

    @property
    def price(self):
        raise NotImplementedError()

    @price.setter
    def price(self, value):
        self._input("price").send_keys(str(value))

    @property
    def fees(self):
        raise NotImplementedError()

    @fees.setter
    def fees(self, value):
        self._input("fees").send_keys(str(value))

    @property
    def isin(self):
        raise NotImplementedError()

    @isin.setter
    def isin(self, value):
        self._input("symbol").send_keys(value)
        suggestions = AutocompleteSuggestions(self.page)
        suggestions.select_best_match()

    @property
    def transaction_type(self):
        raise NotImplementedError()

    @transaction_type.setter
    def transaction_type(self, value):
        select = self.find_element(By.CSS_SELECTOR, 'select[name="transaction"]')
        select.click()
        option = select.find_element(
            By.CSS_SELECTOR, f'option:not([disabled])[value="{value}"]'
        )
        option.click()

    @property
    def date(self):
        raise NotImplementedError()

    @date.setter
    def date(self, value):
        input_element = self.find_element(By.CSS_SELECTOR, "input.picker__input")
        input_element.click()
        DatePicker(self).date = value

    def submit(self):
        button_element = self.find_element(
            By.CSS_SELECTOR, 'button[data-mod-action="add-transaction"]'
        )
        button_element.click()


class PortfolioPage(FtPage):

    URL_TEMPLATE = (
        "https://markets.ft.com/data/portfolio/holdings/full?c={portfolio_id}"
    )

    def toggle_transaction_form(self):
        button_element = self.find_element(
            By.CSS_SELECTOR, 'button[data-mod-action="toggle-add"]'
        )
        button_element.click()
        return AddTransactionForm(self)

    def add_transaction(self, transaction: Transaction):
        form = self.toggle_transaction_form()
        form.quantity = abs(transaction.quantity)
        # form.fees = transaction.fees # TODO fee currency could be different
        form.price = transaction.price
        form.isin = transaction.isin
        form.date = transaction.datetime
        transaction_type = "LongBuy" if transaction.quantity > 0 else "LongSell"
        form.transaction_type = transaction_type
        form.submit()
        sleep(3)

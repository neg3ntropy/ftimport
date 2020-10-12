#!/usr/bin/env python3

import argparse

from degiro import load_transactions
from drivers import get_driver
from pages import PortfolioPage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import transaction to a Financial Times portfolio"
    )
    parser.add_argument(
        "--degiro",
        metavar="FILENAME",
        type=str,
        dest="degiro",
        help="path to an exported CSV from Degiro",
        default="Transactions.csv",
    )
    parser.add_argument(
        "portfolio_id",
        metavar="PORTFOLIO",
        type=str,
        nargs=1,
        help="id of the portfolio to use in ft.com",
    )
    args = parser.parse_args()

    driver = get_driver()
    portfolio_page = PortfolioPage(driver, portfolio_id=args.portfolio_id[0])
    portfolio_page.open()
    for t in load_transactions(args.degiro):
        portfolio_page.add_transaction(t)

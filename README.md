# Strategy Stability Report

A strategy-agnostic toolkit for testing whether backtest expectancy survives time segmentation, transaction-cost stress, drawdowns, and uneven outcome distribution.

## v0.1 contract

Input is a sequence of settled synthetic or user-supplied trade records with timezone-aware `exit_time` and per-trade `gross_return` expressed as a fraction.

The first public report intentionally stays small:
- trade count and gross expectancy
- monthly and quarterly aggregate returns
- fraction of positive months and quarters
- configurable cost scenarios in basis points
- net expectancy, profit factor, cumulative return, and maximum drawdown under each cost scenario

The implementation is dependency-free. It does not contain strategy logic, alpha signals, proprietary datasets, optimization, or claims of statistical significance.

## Why

A profitable aggregate backtest can still be fragile if gains come from one period, disappear after modest costs, or require intolerable drawdowns. This project makes those failure modes explicit with a reproducible report.

## Development

```bash
python -m pip install .
python -m unittest discover -s tests -v
```

All public fixtures are synthetic. CI targets Python 3.10, 3.11, and 3.12.

from collections import defaultdict
from datetime import datetime


def _pf(values):
    gains = sum(x for x in values if x > 0)
    losses = -sum(x for x in values if x < 0)
    if losses == 0:
        return None
    return gains / losses


def _mdd(values):
    equity = peak = 0.0
    worst = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        worst = max(worst, peak - equity)
    return worst


def stability_report(trades, cost_bps=(0, 8, 20)):
    rows = list(trades)
    if not rows:
        raise ValueError("at least one trade is required")
    parsed = []
    for row in rows:
        ts = datetime.fromisoformat(row["exit_time"].replace("Z", "+00:00"))
        if ts.tzinfo is None:
            raise ValueError("exit_time must include timezone")
        gross = float(row["gross_return"])
        parsed.append((ts, gross))
    parsed.sort(key=lambda x: x[0])
    gross_values = [x[1] for x in parsed]
    monthly = defaultdict(list)
    quarterly = defaultdict(list)
    for ts, value in parsed:
        monthly[f"{ts.year:04d}-{ts.month:02d}"].append(value)
        q = (ts.month - 1) // 3 + 1
        quarterly[f"{ts.year:04d}-Q{q}"].append(value)
    scenarios = {}
    for bps in cost_bps:
        drag = bps / 10000.0
        net = [x - drag for x in gross_values]
        scenarios[str(bps)] = {
            "expectancy": sum(net) / len(net),
            "profit_factor": _pf(net),
            "max_drawdown": _mdd(net),
            "total_return": sum(net),
        }
    return {
        "trade_count": len(rows),
        "gross_expectancy": sum(gross_values) / len(gross_values),
        "monthly": {k: sum(v) for k, v in sorted(monthly.items())},
        "quarterly": {k: sum(v) for k, v in sorted(quarterly.items())},
        "positive_month_fraction": sum(sum(v) > 0 for v in monthly.values()) / len(monthly),
        "positive_quarter_fraction": sum(sum(v) > 0 for v in quarterly.values()) / len(quarterly),
        "cost_scenarios_bps": scenarios,
    }

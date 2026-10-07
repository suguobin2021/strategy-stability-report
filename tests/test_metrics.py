import unittest
from strategy_stability_report import stability_report

ROWS = [
 {"exit_time":"2026-01-02T00:00:00Z","gross_return":0.02},
 {"exit_time":"2026-01-03T00:00:00Z","gross_return":-0.01},
 {"exit_time":"2026-02-02T00:00:00Z","gross_return":0.03},
 {"exit_time":"2026-04-02T00:00:00Z","gross_return":-0.005},
]

class Tests(unittest.TestCase):
 def test_counts_and_expectancy(self):
  r=stability_report(ROWS)
  self.assertEqual(r["trade_count"],4)
  self.assertAlmostEqual(r["gross_expectancy"],0.00875)
 def test_month_blocks(self):
  r=stability_report(ROWS)
  self.assertEqual(list(r["monthly"]),["2026-01","2026-02","2026-04"])
  self.assertAlmostEqual(r["positive_month_fraction"],2/3)
 def test_quarter_blocks(self):
  r=stability_report(ROWS)
  self.assertAlmostEqual(r["positive_quarter_fraction"],0.5)
 def test_cost_drag_reduces_expectancy(self):
  r=stability_report(ROWS)
  self.assertGreater(r["cost_scenarios_bps"]["0"]["expectancy"],r["cost_scenarios_bps"]["20"]["expectancy"])
 def test_drawdown_nonnegative(self):
  self.assertGreaterEqual(stability_report(ROWS)["cost_scenarios_bps"]["8"]["max_drawdown"],0)
 def test_empty_rejected(self):
  with self.assertRaises(ValueError): stability_report([])
 def test_naive_timestamp_rejected(self):
  with self.assertRaises(ValueError): stability_report([{"exit_time":"2026-01-01T00:00:00","gross_return":0.1}])

if __name__=="__main__": unittest.main()

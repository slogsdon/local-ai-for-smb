# Cost model foundation

Edit `assumptions.json` for local, cloud or hybrid scenarios. Currency and analysis period are explicit. Null means unknown, not free. Utilization is a fraction from 0 to 1; useful lifetime and analysis period are positive months. All cost/usage inputs are nonnegative. Do not calculate totals with missing inputs.

Future formulas: monthly capital = (acquisition minus residual value) / useful lifetime; electricity = average watts / 1000 × hours × tariff; administration = hours × hourly cost. API token costs = input/output tokens / 1,000,000 × corresponding prices. Request fees and platform charges are separate. Hybrid combines applicable local and cloud categories without counting shared infrastructure twice. Network dependency has qualitative and outage-cost assumptions.

This editable representation establishes categories only. No observed power, current API price, utilization forecast or break-even result is supplied in Phase 0.

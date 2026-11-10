"""PC2 Lab L03-1: Institutional pre-mortem generator and falsification tripwire monitor.

SIMULATED. Implements Gary Klein's (2007) prospective hindsight technique,
generating failure modes across five systematic risk categories and evaluating
observable metric checkpoints against non-negotiable thesis invalidation tripwires.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RiskCategory(StrEnum):
    VARIANT_PERCEPTION = "Variant Perception Invalidation"
    EXECUTION_COSTS = "Execution and Cost Management"
    COMPETITIVE_RESPONSE = "Competitive Response and Pricing"
    BALANCE_SHEET = "Balance Sheet and Liquidity"
    MACRO_CROWDING = "Macro Factor and Crowding Shocks"


class TripwireStatus(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    BREACHED = "BREACHED"


@dataclass(frozen=True)
class FailureMode:
    failure_id: str
    category: RiskCategory
    mechanism: str
    leading_indicator: str
    current_value: float
    warning_threshold: float
    breach_threshold: float
    lower_is_worse: bool

    def evaluate(self, observed_value: float) -> TripwireStatus:
        """Evaluate observed metric against warning and breach thresholds."""
        if self.lower_is_worse:
            if observed_value <= self.breach_threshold:
                return TripwireStatus.BREACHED
            if observed_value <= self.warning_threshold:
                return TripwireStatus.WARNING
            return TripwireStatus.NORMAL
        else:
            if observed_value >= self.breach_threshold:
                return TripwireStatus.BREACHED
            if observed_value >= self.warning_threshold:
                return TripwireStatus.WARNING
            return TripwireStatus.NORMAL


@dataclass(frozen=True)
class PremortemAuditResult:
    total_modes: int
    breached_count: int
    warning_count: int
    normal_count: int
    thesis_status: str
    action_directive: str


def run_premortem_audit(
    modes: list[FailureMode],
    observed_metrics: dict[str, float],
) -> tuple[PremortemAuditResult, list[tuple[FailureMode, float, TripwireStatus]]]:
    """Execute pre-mortem falsification check against current operational metrics."""
    evaluations: list[tuple[FailureMode, float, TripwireStatus]] = []
    breached = 0
    warnings = 0
    normals = 0

    for mode in modes:
        observed = observed_metrics.get(mode.failure_id, mode.current_value)
        status = mode.evaluate(observed)
        if status == TripwireStatus.BREACHED:
            breached += 1
        elif status == TripwireStatus.WARNING:
            warnings += 1
        else:
            normals += 1
        evaluations.append((mode, observed, status))

    if breached > 0:
        thesis_status = "INVALIDATED"
        action_directive = "MANDATORY EXIT: Liquidate position within 1 trading session."
    elif warnings >= 2:
        thesis_status = "UNDER SURVEILLANCE"
        action_directive = "DE-RISK: Cut position size by 50% and demand management explanation."
    else:
        thesis_status = "VALID"
        action_directive = "HOLD / ACCUMULATE: Core thesis metrics intact."

    audit_result = PremortemAuditResult(
        total_modes=len(modes),
        breached_count=breached,
        warning_count=warnings,
        normal_count=normals,
        thesis_status=thesis_status,
        action_directive=action_directive,
    )
    return audit_result, evaluations


def main() -> None:
    print("PC2 Lab L03-1: Institutional Pre-Mortem Generator & Invalidation Monitor")
    print("SIMULATED enterprise software investment thesis pre-mortem")

    failure_modes = [
        FailureMode(
            failure_id="FM-01",
            category=RiskCategory.VARIANT_PERCEPTION,
            mechanism="Net dollar expansion rate decelerates as customers consolidate licenses",
            leading_indicator="Net Retention Rate (NRR %)",
            current_value=122.0,
            warning_threshold=112.0,
            breach_threshold=105.0,
            lower_is_worse=True,
        ),
        FailureMode(
            failure_id="FM-02",
            category=RiskCategory.EXECUTION_COSTS,
            mechanism="Sales & Marketing expenditure spikes without proportional bookings growth",
            leading_indicator="Customer Acquisition Cost (CAC) Payback (months)",
            current_value=14.0,
            warning_threshold=18.0,
            breach_threshold=22.0,
            lower_is_worse=False,
        ),
        FailureMode(
            failure_id="FM-03",
            category=RiskCategory.COMPETITIVE_RESPONSE,
            mechanism="Cloud hyperscaler bundles competitive feature into baseline enterprise contract",
            leading_indicator="Gross Margin Percentage (%)",
            current_value=76.5,
            warning_threshold=72.0,
            breach_threshold=68.0,
            lower_is_worse=True,
        ),
        FailureMode(
            failure_id="FM-04",
            category=RiskCategory.BALANCE_SHEET,
            mechanism="Convertible note maturity refinancing at punitive interest spread",
            leading_indicator="Net Debt / TTM Adjusted EBITDA (x)",
            current_value=1.8,
            warning_threshold=2.8,
            breach_threshold=3.5,
            lower_is_worse=False,
        ),
        FailureMode(
            failure_id="FM-05",
            category=RiskCategory.MACRO_CROWDING,
            mechanism="Hedge fund ownership concentration triggers correlated liquidation",
            leading_indicator="13F Top-10 Institutional Ownership Share (%)",
            current_value=24.0,
            warning_threshold=35.0,
            breach_threshold=45.0,
            lower_is_worse=False,
        ),
    ]

    print(f"Total Pre-Mortem Failure Modes Configured: {len(failure_modes)}")
    print("-" * 84)
    print(f"{'ID':6s} | {'Category':30s} | {'Indicator':22s} | {'Warning':8s} | {'Breach':8s}")
    print("-" * 84)
    for fm in failure_modes:
        print(
            f"{fm.failure_id:6s} | {fm.category.value:30s} | {fm.leading_indicator:22s} | "
            f"{fm.warning_threshold:8.1f} | {fm.breach_threshold:8.1f}"
        )
    print("-" * 84)

    # Simulated Q3 earnings checkpoint data
    checkpoint_q3 = {
        "FM-01": 110.5,  # Warning triggered: NRR fell below 112%
        "FM-02": 16.2,  # Normal
        "FM-03": 74.0,  # Normal
        "FM-04": 2.1,  # Normal
        "FM-05": 38.0,  # Warning triggered: Ownership concentration exceeded 35%
    }

    print("\n--- Quarter 3 Monitoring Checkpoint ---")
    audit, results = run_premortem_audit(failure_modes, checkpoint_q3)
    for fm, obs, status in results:
        print(f"  {fm.failure_id:6s} | {fm.leading_indicator:25s} | Obs: {obs:6.1f} | Status: {status.value:8s}")

    print(
        f"\nAudit Summary: Normal: {audit.normal_count}, Warning: {audit.warning_count}, "
        f"Breached: {audit.breached_count}"
    )
    print(f"Thesis Status:    {audit.thesis_status}")
    print(f"Action Directive: {audit.action_directive}")

    # Simulated catastrophic Q4 checkpoint where FM-01 breaches hard limit
    checkpoint_q4 = {
        "FM-01": 102.0,  # Hard breach: NRR collapsed to 102% (< 105%)
        "FM-02": 23.5,  # Hard breach: CAC payback blew out to 23.5 months (> 22)
        "FM-03": 70.0,  # Warning
        "FM-04": 2.4,  # Normal
        "FM-05": 42.0,  # Warning
    }

    print("\n--- Quarter 4 Monitoring Checkpoint (Catastrophic Scenario) ---")
    audit_q4, results_q4 = run_premortem_audit(failure_modes, checkpoint_q4)
    for fm, obs, status in results_q4:
        print(f"  {fm.failure_id:6s} | {fm.leading_indicator:25s} | Obs: {obs:6.1f} | Status: {status.value:8s}")

    print(
        f"\nAudit Summary: Normal: {audit_q4.normal_count}, Warning: {audit_q4.warning_count}, "
        f"Breached: {audit_q4.breached_count}"
    )
    print(f"Thesis Status:    {audit_q4.thesis_status}")
    print(f"Action Directive: {audit_q4.action_directive}")


main()

"""PC1 Lab L04-1: Presentation slot budget and question reserve arithmetic.

Illustrative plan for a 20-minute expert finance presentation. Not data.
All calculations use exact fractions and integer seconds. Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class SlideAllocation:
    slide_number: int
    topic: str
    minutes: Fraction

    @property
    def seconds(self) -> int:
        return int(self.minutes * 60)


def main() -> None:
    print("PC1 Lab L04-1: Presentation Slot Budget and Question Reserve Arithmetic")
    print("Illustrative plan for an expert presentation. Not data.")

    total_slot_minutes = Fraction(20, 1)  # 20 minutes
    question_reserve_fraction = Fraction(1, 4)  # 25% reserve
    question_reserve_minutes = total_slot_minutes * question_reserve_fraction
    presentation_minutes = total_slot_minutes - question_reserve_minutes

    print(f"Total slot duration: {total_slot_minutes} min ({int(total_slot_minutes * 60)} s)")
    print(
        f"Question and buffer reserve: {question_reserve_minutes} min "
        f"({int(question_reserve_minutes * 60)} s, fraction {question_reserve_fraction})"
    )
    print(
        f"Net presentation delivery time: {presentation_minutes} min "
        f"({int(presentation_minutes * 60)} s, fraction {1 - question_reserve_fraction})"
    )

    # 6-slide expert presentation plan
    slides = [
        SlideAllocation(1, "Core Question & Headline Finding", Fraction(2, 1)),
        SlideAllocation(2, "Institutional Setting & Identification", Fraction(3, 1)),
        SlideAllocation(3, "Primary Empirical Result & Standalone Figure", Fraction(4, 1)),
        SlideAllocation(4, "Economic Mechanism & Channels", Fraction(3, 1)),
        SlideAllocation(5, "Steelmanned Strongest Objection & Robustness", Fraction(2, 1)),
        SlideAllocation(6, "Concluding Takeaway & Policy Implications", Fraction(1, 1)),
    ]

    print("\nSlide Schedule:")
    print(f"{'Slide':5s} | {'Topic':45s} | {'Minutes':7s} | {'Seconds':7s} | {'Share of Talk':13s}")
    print("-" * 88)

    sum_slide_minutes = Fraction(0, 1)
    for s in slides:
        sum_slide_minutes += s.minutes
        share = s.minutes / presentation_minutes
        print(
            f"{s.slide_number:5d} | {s.topic:45s} | {float(s.minutes):7.1f} | "
            f"{s.seconds:7d} | {float(share) * 100:6.1f}% ({share})"
        )

    print("-" * 88)
    print(f"Total planned slide time: {sum_slide_minutes} min ({int(sum_slide_minutes * 60)} s)")
    matches_delivery_budget = sum_slide_minutes == presentation_minutes
    print(f"Slide time exactly matches delivery budget: {matches_delivery_budget}")

    num_slides = len(slides)
    avg_minutes_per_slide = presentation_minutes / num_slides
    print(f"Total slide count: {num_slides}")
    print(
        f"Average pace per slide: {avg_minutes_per_slide} min/slide "
        f"({float(avg_minutes_per_slide):.2f} min/slide, {int(avg_minutes_per_slide * 60)} s/slide)"
    )

    # Rules validation
    pace_ok = Fraction(3, 2) <= avg_minutes_per_slide <= Fraction(3, 1)
    reserve_ok = question_reserve_minutes >= Fraction(5, 1)
    objection_included = any("objection" in s.topic.lower() for s in slides)

    print(f"Rule check: Pace between 1.5 and 3.0 min/slide: {pace_ok}")
    print(f"Rule check: Question reserve >= 5 min: {reserve_ok}")
    print(f"Rule check: Explicit objection/robustness slide: {objection_included}")


main()

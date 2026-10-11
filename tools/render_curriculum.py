#!/usr/bin/env python3
"""Validate the curriculum sources and render curriculum.json + CURRICULUM.md.

The curriculum is authored as YAML under ``curriculum/``. This script is the
single gate between those sources and everything downstream (the site's
program map, the builder prompts, the hour budgets). It fails with a non-zero
exit code on any structural defect:

* duplicate or malformed module IDs
* a prerequisite that does not exist
* a cycle in the prerequisite graph
* a module whose tier is below one of its prerequisites' tiers
* a module without a project, or with an unknown grading mode
* a studio whose required modules sit above the studio's declared tier
* Atlas milestones that do not match the module that delivers them
* a credential whose prerequisite closure exceeds its tier, whose studios need
  modules outside the closure, or whose course map points outside the closure
* a body-of-knowledge coverage map that names an unknown module

Usage::

    python3 tools/render_curriculum.py            # validate + render
    python3 tools/render_curriculum.py --check    # validate only
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_DIR = ROOT / "curriculum"
JSON_OUT = CURRICULUM_DIR / "curriculum.json"
MD_OUT = ROOT / "CURRICULUM.md"

GRADING_MODES = frozenset({"autograder", "rubric", "both"})
REQUIRED_MODULE_KEYS = ("id", "title", "tier", "hours", "prereqs", "core", "sources", "lab", "project")
REQUIRED_PROJECT_KEYS = ("title", "brief", "deliverable", "grading")
REQUIRED_STUDIO_KEYS = ("id", "title", "tier", "requires", "hours", "grading", "brief", "deliverables")
# U.S. federal credit-hour definition (34 CFR 600.2): one credit is roughly one
# hour of instruction plus two hours of out-of-class work per week over a
# ~15-week semester, i.e. ~45 hours of student work. A 3-credit course is ~135 h.
HOURS_PER_CREDIT = 45
HOURS_PER_COURSE = 3 * HOURS_PER_CREDIT
STUDY_HOURS_PER_WEEK = 45
STUDY_WEEKS_PER_YEAR = 48


class CurriculumError(Exception):
    """Raised when the curriculum sources violate a structural invariant."""


@dataclass(frozen=True)
class Tier:
    code: str
    rank: int
    name: str
    standard: str


@dataclass
class Module:
    id: str
    title: str
    tier: str
    hours: int
    prereqs: list[str]
    part_code: str
    raw: dict[str, Any]


@dataclass
class Part:
    order: int
    code: str
    title: str
    studio: dict[str, Any] | None
    modules: list[Module] = field(default_factory=list)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise CurriculumError(f"{path.name}: top level must be a mapping")
    return data


def load_sources() -> tuple[dict[str, Any], list[Part]]:
    meta = load_yaml(CURRICULUM_DIR / "meta.yaml")
    parts: list[Part] = []
    for path in sorted(CURRICULUM_DIR.glob("[0-9][0-9]-*.yaml")):
        for raw_part in load_yaml(path).get("parts", []):
            part = Part(
                order=int(raw_part["order"]),
                code=str(raw_part["code"]),
                title=str(raw_part["title"]),
                studio=raw_part.get("studio"),
            )
            for raw_module in raw_part.get("modules", []):
                missing = [key for key in REQUIRED_MODULE_KEYS if key not in raw_module]
                if missing:
                    raise CurriculumError(f"{path.name}: module {raw_module.get('id', '?')} missing {missing}")
                part.modules.append(
                    Module(
                        id=str(raw_module["id"]),
                        title=str(raw_module["title"]),
                        tier=str(raw_module["tier"]),
                        hours=int(raw_module["hours"]),
                        prereqs=[str(p) for p in raw_module["prereqs"]],
                        part_code=part.code,
                        raw=raw_module,
                    )
                )
            parts.append(part)
    parts.sort(key=lambda p: p.order)
    return meta, parts


def validate(meta: dict[str, Any], parts: list[Part]) -> tuple[dict[str, Tier], dict[str, Module], list[str]]:
    errors: list[str] = []
    tiers = {t["code"]: Tier(t["code"], int(t["rank"]), t["name"], t["standard"]) for t in meta["tiers"]}

    orders = [p.order for p in parts]
    if len(orders) != len(set(orders)):
        errors.append("duplicate part order values")

    modules: dict[str, Module] = {}
    for part in parts:
        if part.code not in {"P0", "CAP"} and not part.studio:
            errors.append(f"part {part.code}: missing studio project")
        if part.studio:
            missing = [key for key in REQUIRED_STUDIO_KEYS if key not in part.studio]
            if missing:
                errors.append(f"part {part.code}: studio missing {missing}")
            elif part.studio["grading"] not in GRADING_MODES:
                errors.append(f"part {part.code}: studio grading must be one of {sorted(GRADING_MODES)}")
            elif part.studio["tier"] not in tiers:
                errors.append(f"part {part.code}: studio has unknown tier {part.studio['tier']}")
        for module in part.modules:
            if module.id in modules:
                errors.append(f"duplicate module id {module.id}")
            modules[module.id] = module
            if module.tier not in tiers:
                errors.append(f"{module.id}: unknown tier {module.tier}")
            if module.hours <= 0:
                errors.append(f"{module.id}: hours must be positive")
            if not module.raw["sources"]:
                errors.append(f"{module.id}: at least one source is required")
            project = module.raw["project"]
            missing = [key for key in REQUIRED_PROJECT_KEYS if not project.get(key)]
            if missing:
                errors.append(f"{module.id}: project missing {missing}")
            if project.get("grading") not in GRADING_MODES:
                errors.append(f"{module.id}: project grading must be one of {sorted(GRADING_MODES)}")

    for module in modules.values():
        for prereq in module.prereqs:
            if prereq not in modules:
                errors.append(f"{module.id}: unknown prerequisite {prereq}")
                continue
            if module.id == prereq:
                errors.append(f"{module.id}: lists itself as a prerequisite")
            if module.tier in tiers and modules[prereq].tier in tiers:
                if tiers[modules[prereq].tier].rank > tiers[module.tier].rank:
                    errors.append(
                        f"{module.id} (tier {module.tier}) depends on {prereq} (tier {modules[prereq].tier}): "
                        "a module cannot sit below its prerequisites"
                    )

    for part in parts:
        studio = part.studio
        if not studio or any(key not in studio for key in REQUIRED_STUDIO_KEYS) or studio["tier"] not in tiers:
            continue
        for required in studio["requires"]:
            if required not in modules:
                errors.append(f"{studio['id']}: requires unknown module {required}")
            elif tiers[modules[required].tier].rank > tiers[studio["tier"]].rank:
                errors.append(
                    f"{studio['id']} (tier {studio['tier']}) requires {required} (tier {modules[required].tier})"
                )

    milestone_ids = set()
    for milestone in meta.get("milestones", []):
        milestone_ids.add(milestone["id"])
        for code in milestone["tiers"]:
            if code not in tiers:
                errors.append(f"milestone {milestone['id']}: unknown tier {code}")
        for excluded in milestone.get("exclude", []):
            if excluded not in modules:
                errors.append(f"milestone {milestone['id']}: excludes unknown module {excluded}")

    atlas_by_module = {m.id: m.raw["project"].get("atlas") for m in modules.values() if m.raw["project"].get("atlas")}
    declared = {a["id"]: a["module"] for a in meta.get("atlas", [])}
    for atlas_id, module_id in declared.items():
        if module_id not in modules:
            errors.append(f"atlas {atlas_id}: module {module_id} does not exist")
        elif atlas_by_module.get(module_id) != atlas_id:
            errors.append(f"atlas {atlas_id}: module {module_id} project is not tagged atlas: {atlas_id}")
    for module_id, atlas_id in atlas_by_module.items():
        if declared.get(atlas_id) != module_id:
            errors.append(f"{module_id}: project tagged {atlas_id} but meta.yaml assigns it elsewhere")

    for track in meta.get("tracks", []):
        for target in track["targets"]:
            if target not in modules:
                errors.append(f"track {track['id']}: unknown target {target}")

    for body in meta.get("bodies_of_knowledge", []):
        for topic in body["topics"]:
            for module_id in topic["modules"]:
                if module_id not in modules:
                    errors.append(f"{body['id']} topic '{topic['topic']}': unknown module {module_id}")

    order: list[str] = []
    if not errors:
        try:
            order = list(TopologicalSorter({m.id: m.prereqs for m in modules.values()}).static_order())
        except CycleError as exc:
            errors.append(f"prerequisite cycle: {' -> '.join(exc.args[1])}")
    if not errors:
        errors.extend(validate_credentials(meta, parts, tiers, modules))

    if errors:
        raise CurriculumError("\n".join(f"  - {e}" for e in errors))
    return tiers, modules, order


def validate_credentials(
    meta: dict[str, Any], parts: list[Part], tiers: dict[str, Tier], modules: dict[str, Module]
) -> list[str]:
    """Check every credential is a coherent, tier-bounded view over the DAG."""
    errors: list[str] = []
    studios = {p.studio["id"]: p.studio for p in parts if p.studio}
    for cred in meta.get("credentials", []):
        cid = cred["id"]
        unknown = [m for m in cred["requires"] if m not in modules]
        if unknown:
            errors.append(f"credential {cid}: unknown modules {unknown}")
            continue
        if cred["max_tier"] not in tiers:
            errors.append(f"credential {cid}: unknown max_tier {cred['max_tier']}")
            continue
        required = closure(cred["requires"], modules)
        ceiling = tiers[cred["max_tier"]].rank
        for module_id in sorted(required):
            if tiers[modules[module_id].tier].rank > ceiling:
                errors.append(
                    f"credential {cid} (max tier {cred['max_tier']}) pulls in {module_id} (tier {modules[module_id].tier})"
                )
        for studio_id in cred["studios"]:
            if studio_id not in studios:
                errors.append(f"credential {cid}: unknown studio {studio_id}")
                continue
            outside = [m for m in studios[studio_id]["requires"] if m not in required]
            if outside:
                errors.append(f"credential {cid}: {studio_id} needs modules outside the closure {outside}")
        for entry in cred.get("course_map", []):
            outside = [m for m in entry["modules"] if m not in required]
            if outside:
                errors.append(f"credential {cid}: course '{entry['course']}' maps outside the closure {outside}")
    return errors


def closure(targets: list[str], modules: dict[str, Module]) -> set[str]:
    seen: set[str] = set()
    stack = list(targets)
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(modules[current].prereqs)
    return seen


def full_time_years(hours: int) -> float:
    return hours / (STUDY_HOURS_PER_WEEK * STUDY_WEEKS_PER_YEAR)


def compute_stats(
    meta: dict[str, Any], parts: list[Part], tiers: dict[str, Tier], modules: dict[str, Module]
) -> dict[str, Any]:
    module_hours_by_tier: dict[str, int] = defaultdict(int)
    module_count_by_tier: dict[str, int] = defaultdict(int)
    for module in modules.values():
        module_hours_by_tier[module.tier] += module.hours
        module_count_by_tier[module.tier] += 1

    studio_hours_by_tier: dict[str, int] = defaultdict(int)
    for part in parts:
        if part.studio:
            studio_hours_by_tier[part.studio["tier"]] += int(part.studio["hours"])

    milestone_hours: dict[str, int] = {}
    for milestone in meta["milestones"]:
        included = set(milestone["tiers"])
        excluded = set(milestone.get("exclude", []))
        hours = sum(m.hours for m in modules.values() if m.tier in included and m.id not in excluded)
        hours += sum(int(p.studio["hours"]) for p in parts if p.studio and p.studio["tier"] in included)
        milestone_hours[milestone["id"]] = hours

    track_stats = []
    for track in meta["tracks"]:
        required = closure(track["targets"], modules)
        hours = sum(modules[m].hours for m in required)
        track_stats.append(
            {
                "id": track["id"],
                "name": track["name"],
                "targets": track["targets"],
                "modules": len(required),
                "hours": hours,
                "full_time_years": round(full_time_years(hours), 2),
            }
        )

    studio_hours = {p.studio["id"]: int(p.studio["hours"]) for p in parts if p.studio}
    credential_stats = []
    for cred in meta.get("credentials", []):
        required = closure(cred["requires"], modules)
        mapped = {m for entry in cred.get("course_map", []) for m in entry["modules"]}
        module_hours = sum(modules[m].hours for m in required)
        cred_studio_hours = sum(studio_hours[s] for s in cred["studios"])
        hours = module_hours + cred_studio_hours
        credential_stats.append(
            {
                "id": cred["id"],
                "name": cred["name"],
                "level": cred["level"],
                "modules": len(required),
                "studios": len(cred["studios"]),
                "projects": len(required) + len(cred["studios"]),
                "module_hours": module_hours,
                "studio_hours": cred_studio_hours,
                "hours": hours,
                "full_time_years": round(full_time_years(hours), 2),
                "credit_equivalent": round(hours / HOURS_PER_CREDIT),
                "closure": sorted(required, key=lambda m: (modules[m].part_code, m)),
                "supporting": sorted(required - mapped, key=lambda m: (modules[m].part_code, m)),
            }
        )

    total_hours = sum(module_hours_by_tier.values()) + sum(studio_hours_by_tier.values())
    projects = len(modules) + sum(1 for p in parts if p.studio)
    return {
        "modules": len(modules),
        "parts": len(parts),
        "projects": projects,
        "studios": sum(1 for p in parts if p.studio),
        "atlas_milestones": len(meta.get("atlas", [])),
        "module_count_by_tier": dict(module_count_by_tier),
        "module_hours_by_tier": dict(module_hours_by_tier),
        "studio_hours_by_tier": dict(studio_hours_by_tier),
        "milestone_hours": milestone_hours,
        "total_hours": total_hours,
        "full_time_years": round(full_time_years(total_hours), 2),
        "credit_hour_equivalent": round(total_hours / HOURS_PER_CREDIT),
        "course_equivalent": round(total_hours / HOURS_PER_COURSE),
        "tracks": track_stats,
        "credentials": credential_stats,
    }


def render_json(meta: dict[str, Any], parts: list[Part], order: list[str], stats: dict[str, Any]) -> str:
    payload = {
        "program": meta["program"],
        "tiers": meta["tiers"],
        "milestones": meta["milestones"],
        "tracks": meta["tracks"],
        "atlas": meta["atlas"],
        "credentials": meta.get("credentials", []),
        "bodies_of_knowledge": meta.get("bodies_of_knowledge", []),
        "topological_order": order,
        "stats": stats,
        "parts": [
            {
                "order": part.order,
                "code": part.code,
                "title": part.title,
                "studio": part.studio,
                "modules": [module.raw | {"part": part.code} for module in part.modules],
            }
            for part in parts
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def md_escape(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def render_markdown(
    meta: dict[str, Any], parts: list[Part], tiers: dict[str, Tier], modules: dict[str, Module], stats: dict[str, Any]
) -> str:
    program = meta["program"]
    ranked = sorted(tiers.values(), key=lambda t: t.rank)
    out: list[str] = []
    out.append(f"# Curriculum — {program['name']}\n")
    out.append(
        f"> **Generated** by `tools/render_curriculum.py` from `curriculum/*.yaml` "
        f"(v{program['version']}, {program['date']}). Do not edit by hand.\n"
    )
    out.append("## Program at a glance\n")
    out.append("| Measure | Value |\n|---|---|")
    out.append(f"| Parts | {stats['parts']} |")
    out.append(f"| Modules | {stats['modules']} |")
    out.append(
        f"| Graded projects | {stats['projects']} "
        f"({stats['modules']} module projects + {stats['studios']} studio projects) |"
    )
    out.append(f"| Atlas milestones | {stats['atlas_milestones']} |")
    out.append(f"| Total design hours | {stats['total_hours']:,} |")
    out.append(
        f"| Credit-hour equivalent | ≈{stats['credit_hour_equivalent']:,} credits "
        f"(≈{stats['course_equivalent']} three-credit courses at {HOURS_PER_COURSE} h each) |"
    )
    out.append(
        f"| Full-time equivalent | {stats['full_time_years']} years at "
        f"{STUDY_HOURS_PER_WEEK} h/week × {STUDY_WEEKS_PER_YEAR} weeks |\n"
    )
    out.append(
        "Hours are design targets that include each module's project. They are "
        f"calibrated against the U.S. federal credit-hour definition ({HOURS_PER_CREDIT} h of "
        f"student work per credit, {HOURS_PER_COURSE} h per three-credit course), will be "
        "recalibrated against pilot-learner data, and shrink for any student who tests out "
        "of material through placement.\n"
    )

    out.extend(render_credentials(meta, modules, stats))
    out.append("## Tiers\n")
    out.append("| Tier | Standard | Modules | Module h | Studio h |")
    out.append("|---|---|---|---|---|")
    for tier in ranked:
        out.append(
            f"| **{tier.code}** {tier.name} | {md_escape(tier.standard)} | "
            f"{stats['module_count_by_tier'].get(tier.code, 0)} | "
            f"{stats['module_hours_by_tier'].get(tier.code, 0):,} | "
            f"{stats['studio_hours_by_tier'].get(tier.code, 0):,} |"
        )
    out.append("")
    out.append("## Milestones (cumulative)\n")
    out.append("| Milestone | Rule | Cumulative h | FTE years |")
    out.append("|---|---|---|---|")
    for milestone in meta["milestones"]:
        cum = stats["milestone_hours"][milestone["id"]]
        out.append(f"| **{milestone['name']}** | {md_escape(milestone['rule'])} | {cum:,} | {full_time_years(cum):.2f} |")
    out.append("")

    out.append("## Career tracks (computed prerequisite closures)\n")
    out.append("| Track | Targets | Modules required | Module hours | FTE years |")
    out.append("|---|---|---|---|---|")
    for track in stats["tracks"]:
        out.append(
            f"| {track['name']} | {', '.join(track['targets'])} | {track['modules']} | "
            f"{track['hours']:,} | {track['full_time_years']:.2f} |"
        )
    out.append("")

    out.append("## Atlas — the program-long build\n")
    out.append("| Milestone | Delivered in | Title | Delivers |")
    out.append("|---|---|---|---|")
    for item in meta["atlas"]:
        out.append(f"| {item['id']} | {item['module']} | {item['title']} | {md_escape(item['delivers'])} |")
    out.append("")

    out.append("## Modules by part\n")
    out.append("Legend: tier **F/U/M/D** · hours · ← prerequisites · grading `auto` / `rubric` / `both` · ⚑ Atlas milestone · ⚖ debate.\n")
    for part in parts:
        out.append(f"### Part {part.order} · {part.title} (`{part.code}`)\n")
        if part.studio:
            s = part.studio
            out.append(
                f"**Studio · {s['title']}** · {s['tier']} · {s['hours']} h · ← {', '.join(s['requires'])} · `{s['grading']}`  \n"
                f"{md_escape(s['brief'])}  \n"
                f"*Deliverables:* {', '.join(s['deliverables'])}\n"
            )
        for module in part.modules:
            raw = module.raw
            project = raw["project"]
            prereqs = ", ".join(module.prereqs) if module.prereqs else "none"
            atlas = f" · ⚑ {project['atlas']}" if project.get("atlas") else ""
            debate = f"\n  - ⚖ *Debate:* {md_escape(raw['debate'])}" if raw.get("debate") else ""
            out.append(
                f"- **{module.id} · {module.title}** · {module.tier} · {module.hours} h · ← {prereqs}{atlas}\n"
                f"  - *Core:* {md_escape(raw['core'])}\n"
                f"  - *Sources:* {'; '.join(md_escape(s) for s in raw['sources'])}\n"
                f"  - *Lab:* {md_escape(raw['lab'])}\n"
                f"  - *Project — {project['title']}* (`{project['grading']}`): {md_escape(project['brief'])} "
                f"*Deliverable:* {md_escape(project['deliverable'])}"
                f"{debate}"
            )
        out.append("")
    return "\n".join(out)


def render_credentials(meta: dict[str, Any], modules: dict[str, Module], stats: dict[str, Any]) -> list[str]:
    out: list[str] = []
    out.append("## Degree-equivalent credentials\n")
    out.append(
        "Named credentials are explicit views over the curriculum graph. The validator proves "
        "each one closed under prerequisites and bounded by its tier. They are **content-equivalent "
        "only**: only an accredited, state-authorized institution can award a degree.\n"
    )
    out.append("| Credential | Modules | Studios | Graded projects | Hours | Credit equivalent | FTE years |")
    out.append("|---|---|---|---|---|---|---|")
    for cs in stats["credentials"]:
        out.append(
            f"| **{cs['name']}** | {cs['modules']} | {cs['studios']} | {cs['projects']} | {cs['hours']:,} | "
            f"≈{cs['credit_equivalent']} credits | {cs['full_time_years']:.2f} |"
        )
    out.append(
        "\nCredential hours include every prerequisite the credential pulls in. Credentials overlap: "
        "a student completing the Master's has already completed most of the Bachelor's.\n"
    )
    by_id = {cs["id"]: cs for cs in stats["credentials"]}
    for cred in meta.get("credentials", []):
        cs = by_id[cred["id"]]
        out.append(f"### {cred['name']}\n")
        out.append("| Area | Course | Program modules | Hours |")
        out.append("|---|---|---|---|")
        for entry in cred["course_map"]:
            names = "<br>".join(f"{m} · {modules[m].title}" for m in entry["modules"])
            hours = sum(modules[m].hours for m in entry["modules"])
            out.append(f"| {entry['group']} | **{entry['course']}** | {names} | {hours} |")
        out.append("")
        out.append(f"*Studios:* {', '.join(cred['studios'])}  ")
        if cs["supporting"]:
            out.append(f"*Supporting prerequisites pulled in by the graph:* {', '.join(cs['supporting'])}")
        out.append("")
    for body in meta.get("bodies_of_knowledge", []):
        out.append(f"### External coverage check: {body['name']}\n")
        out.append("| Topic area | Covered by |")
        out.append("|---|---|")
        for topic in body["topics"]:
            names = "<br>".join(f"{m} · {modules[m].title}" for m in topic["modules"])
            out.append(f"| {topic['topic']} | {names} |")
        out.append("")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only; do not write outputs")
    args = parser.parse_args()

    try:
        meta, parts = load_sources()
        tiers, modules, order = validate(meta, parts)
    except CurriculumError as exc:
        print(f"curriculum invalid:\n{exc}", file=sys.stderr)
        return 1

    stats = compute_stats(meta, parts, tiers, modules)
    print(
        f"curriculum valid: {stats['parts']} parts, {stats['modules']} modules, "
        f"{stats['projects']} projects, {stats['total_hours']:,} h "
        f"({stats['full_time_years']} FTE years)"
    )
    if args.check:
        return 0

    JSON_OUT.write_text(render_json(meta, parts, order, stats), encoding="utf-8")
    MD_OUT.write_text(render_markdown(meta, parts, tiers, modules, stats), encoding="utf-8")
    print(f"wrote {JSON_OUT.relative_to(ROOT)} and {MD_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# agent-team decisions cache

## 2026-05-26 — market-report research run

**task_pattern**: generate full market analysis report (research + analysis + format)
**agents**: [researcher, analyst, formatter]
**reasoning**: Task covers all three roles with real DAG dependencies; all agents required.
**agents_hash**: researcher.md+analyst.md+formatter.md (3 files, research kind)
**config_hash**: kind=research,mode=commander,isolation=directory-fork,publish_strategy=overlay

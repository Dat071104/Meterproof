#!/usr/bin/env python3
"""Structural overlay validator. Not a substitute for real DE acceptance tests."""
from pathlib import Path
from xml.etree import ElementTree as ET
import argparse
import json
import re
import sys

PHASES={
  'core':['P'+str(i) for i in range(8)],
  'lite':['L'+str(i) for i in range(4)],
  'atlas':['A'+str(i) for i in range(6)],
  'adoption':['U'+str(i) for i in range(3)],
}
SKILLS=['meterproof-evidence','meterproof-differential-replay','meterproof-failure-drills','meterproof-architecture','atlas-ai-grounding']
SCHEMAS=['source_receipt.v1.schema.json','replay_manifest.v1.schema.json','verification_decision.v1.schema.json','published_read_report.v1.schema.json']
STATUSES={'NOT_STARTED','IN_PROGRESS','BLOCKED','FAILED','PASS','HUMAN_GO','HUMAN_CONDITIONAL_GO','HUMAN_NO_GO'}
PASSING={'PASS','HUMAN_GO','HUMAN_CONDITIONAL_GO'}
BOUNDARIES=['services/ingestion_api','services/durable_worker','services/verification_api','services/publication','core/evidence','core/policy_spec','core/replay','core/comparator','pipelines/dbt','pipelines/debezium','pipelines/flink_java','independent_oracle','products/lite','products/atlas','infra/compose','infra/cloud','tests/fault']

def main():
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser()
    p.add_argument('--target',type=Path,default=Path.cwd())
    args=p.parse_args()
    repo=args.target.resolve()
    errors=[]
    paths=[
      'docs/METERPROOF_START_HERE.md',
      'docs/architecture/ARCHITECTURE_DECISIONS.md',
      'docs/architecture/SOURCE_CUT_PROTOCOL.md',
      'docs/architecture/METERPROOF_CORE_ATLAS_LITE.drawio',
      'docs/architecture/REPOSITORY_STRUCTURE.md',
      'docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md',
      'docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md',
      'docs/milestones/MILESTONE_INDEX.md',
      'docs/milestones/milestones.json',
      'docs/ops/PROJECT_STATUS.md',
      'docs/gates/GATE_RECEIPT_TEMPLATE.md',
    ]
    for cat,items in PHASES.items():
        paths.extend(f'docs/milestones/{cat}/{id}.md' for id in items)
    paths.extend(f'.agents/skills/{s}/SKILL.md' for s in SKILLS)
    paths.extend(f'.claude/skills/{s}/SKILL.md' for s in SKILLS)
    paths.extend(f'contracts/jsonschema/{s}' for s in SCHEMAS)
    paths.extend(f'{b}/ARCHITECTURE_BOUNDARY.md' for b in BOUNDARIES)
    for relative in paths:
        if not (repo/relative).is_file():
            errors.append('MISSING '+relative)
    if not (repo/'AGENTS.md').exists():
        errors.append('MISSING existing pack root AGENTS.md')
    if errors:
        for e in errors:print('FAIL',e)
        return 2
    try:
        reg=json.loads((repo/'docs/milestones/milestones.json').read_text(encoding='utf-8'))
        records=reg['milestones']
        assert len(records)==21, 'expected 21 milestones'
        assert sum(len(r['subphases']) for r in records)==82, 'expected 82 subphases'
        # Statuses may advance as real work happens; a passing status must point at a gate receipt.
        for r in records:
            assert r['status'] in STATUSES, f"{r['id']} unknown status {r['status']}"
            if r['status'] in PASSING:
                receipt=repo/f"docs/gates/{r['gate']}/{r['gate']}_GATE_RECEIPT.md"
                assert receipt.is_file(), f"{r['id']} is {r['status']} without docs/gates/{r['gate']}/{r['gate']}_GATE_RECEIPT.md"
        assert len({r['id'] for r in records})==21, 'duplicate phase ID'
        for r in records:
            card=(repo/f"docs/milestones/{r['area'].lower()}/{r['id']}.md").read_text(encoding='utf-8')
            assert all(id in card for id in r['subphases']), r['id']+' subphase missing'
            assert r['gate'] in card, r['id']+' gate missing'
            assert '**Verification:**' in card, r['id']+' no verification'
        for s in SKILLS:
            md=(repo/f'.agents/skills/{s}/SKILL.md').read_text(encoding='utf-8')
            assert md.startswith('---\n'), s+' no YAML frontmatter'
            assert 'name: '+s in md.split('---',2)[1],s+' name mismatch'
        for name in SCHEMAS:
            doc=json.loads((repo/f'contracts/jsonschema/{name}').read_text(encoding='utf-8'))
            assert doc.get('$schema','').endswith('2020-12/schema'),name+' unsupported schema meta'
            assert 'required' in doc and 'properties' in doc,name+' missing contract'
            try:
                import jsonschema  # type: ignore[import-untyped]
            except ImportError:
                pass
            else:
                jsonschema.Draft202012Validator.check_schema(doc)
        draw=ET.parse(repo/'docs/architecture/METERPROOF_CORE_ATLAS_LITE.drawio').getroot()
        assert draw.tag=='mxfile' and len(draw.findall('diagram'))>=2, 'drawio needs 2 editable pages'
        faults=(repo/'docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md').read_text(encoding='utf-8')
        assert all(('T'+str(i).zfill(2)) in faults for i in range(1,13)), 'T01–T12 missing'
        assert 'AGENTS' in (repo/'docs/METERPROOF_START_HERE.md').read_text(encoding='utf-8')
    except Exception as ex:
        print('FAIL validation:',ex)
        return 3
    print('PASS structural validation: 21 phase cards / 82 subphases, 5 domain skills + Claude adapters, 4 JSON schemas, 2-page editable draw.io, 12 specified fault cases.')
    print('IMPORTANT: This does NOT prove Core pipeline tests, user adoption, Flink recovery, or G0–G7 passed.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())

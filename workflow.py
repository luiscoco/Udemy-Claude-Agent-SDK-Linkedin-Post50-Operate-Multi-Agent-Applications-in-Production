"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    assessment = await agent.ask('release_review', 'Assess the candidate release using the supplied health evidence. Do not claim it was deployed.', data,
                                 {'ready': False, 'reason': 'The candidate health check failed.'})
    activate = data['candidate_health'] and assessment['ready']
    decision = {'previous': data['active'], 'selected': data['candidate'] if activate else data['active'],
                'action': 'activate_local_candidate' if activate else 'keep_previous', 'real_deployment_changed': False}
    atomic_json(agent.output / 'release_decision.json', decision)
    return {'review': assessment, 'decision': decision}

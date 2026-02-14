#!/usr/bin/env python3
"""One-time script to add topics:: field to all publication .txt files."""

import os

# Mapping of paper_id -> list of topic slugs
PAPER_TOPICS = {
    # 2025
    'iccv25lightswitch': ['neural-rendering'],
    'corl25gen2act': ['robot-learning'],
    'cvpr25diffusionsfm': ['3d-reconstruction'],
    'cvpr25uniphy': ['physics-dynamics'],
    'cvpr25aerialmegadepth': ['3d-reconstruction'],
    'cvpr25turbo3d': ['3d-reconstruction', 'generative-models'],
    'cvpr25scenefactor': ['generative-models', '3d-reconstruction'],
    '3dv25materialfusion': ['neural-rendering'],
    '3dv25dressrecon': ['3d-reconstruction'],
    # 2024
    'neurips24ags': ['3d-reconstruction'],
    'eccv24track2act': ['robot-learning'],
    'eccv24upfusion': ['3d-reconstruction', 'generative-models'],
    'cvpr24ghop': ['3d-reconstruction', 'object-understanding'],
    'cvpr24mvdfusion': ['3d-reconstruction', 'generative-models'],
    'iclr24rays': ['3d-reconstruction'],
    'icra24hopman': ['robot-learning'],
    'icra24roboagent': ['robot-learning'],
    '3dv24relposepp': ['3d-reconstruction'],
    # 2023
    'iccv23diffhoi': ['3d-reconstruction', 'object-understanding'],
    'iccv23control': ['robot-learning'],
    'iccv23texture': ['neural-rendering', 'generative-models'],
    'icra23affordance': ['robot-learning'],
    'iclr23analogical': ['object-understanding'],
    'cvpr23sparsefusion': ['3d-reconstruction', 'generative-models'],
    'cvpr23affordance': ['object-understanding', 'generative-models'],
    # 2022
    'neurips22dycheck': ['neural-rendering'],
    'eccv22relpose': ['3d-reconstruction'],
    'cvpr22ss3d': ['3d-reconstruction'],
    'cvpr22ihoi': ['3d-reconstruction', 'object-understanding'],
    'cvpr22autosdf': ['3d-reconstruction', 'generative-models'],
    # 2021
    'neurips21ners': ['neural-rendering', '3d-reconstruction'],
    'neurips21nrns': ['robot-learning'],
    'corl21planar': ['robot-learning', 'physics-dynamics'],
    'iccv21act': ['robot-learning', 'object-understanding'],
    'icml21pixel': ['generative-models'],
    'cvpr21mesh': ['3d-reconstruction', 'object-understanding'],
    # 2020
    'neurips20audio': ['robot-learning'],
    'corl20vime': ['robot-learning'],
    'cvpr20acsm': ['object-understanding'],
    'cvpr20force': ['physics-dynamics'],
    'iclr20synergy': ['robot-learning'],
    'iclr20motor': ['robot-learning'],
    'icra20schema': ['robot-learning'],
    # 2019
    'corl19ocm': ['physics-dynamics', 'robot-learning'],
    'iccv19csm': ['object-understanding'],
    'iccv19cvp': ['physics-dynamics', 'generative-models'],
    'iccv19relnet': ['3d-reconstruction', 'object-understanding'],
    'iccv19craft': ['generative-models'],
    'arxiv19mvs': ['3d-reconstruction'],
    # 2018
    'eccv18lsi': ['3d-reconstruction', 'neural-rendering'],
    'eccv18cmr': ['3d-reconstruction', 'object-understanding'],
    'cvpr18mvc': ['3d-reconstruction'],
    'cvpr18f3d': ['3d-reconstruction'],
    # 2017
    'cvpr17drc': ['3d-reconstruction'],
    'cvpr17abstraction': ['3d-reconstruction', 'object-understanding'],
    '3dv17hsp': ['3d-reconstruction'],
    # 2016
    'pami16reconstruction': ['3d-reconstruction', 'object-understanding'],
    'eccv16flow': ['neural-rendering'],
    # 2015
    'iccv15pose': ['object-understanding'],
    'iccv15amodal': ['object-understanding'],
    'cvpr15vps': ['object-understanding'],
    'cvpr15csdm': ['3d-reconstruction', 'object-understanding'],
    'cvpr15vvn': ['3d-reconstruction'],
    # 2013
    'uist13colors': [],
    # PAMI journal versions (not in main list but files exist)
    'pami19drc': ['3d-reconstruction'],
    'pami19hsp': ['3d-reconstruction'],
}

def add_topics(pub_dir):
    for fname in os.listdir(pub_dir):
        if not fname.endswith('.txt'):
            continue
        paper_id = fname[:-4]
        if paper_id not in PAPER_TOPICS:
            print(f"WARNING: No topics defined for {paper_id}")
            continue

        fpath = os.path.join(pub_dir, fname)
        with open(fpath, 'r') as f:
            content = f.read()

        # Skip if topics already added
        if 'topics::' in content:
            continue

        topics = ', '.join(PAPER_TOPICS[paper_id])
        # Add topics line before the end of the file
        content = content.rstrip() + '\n'
        content += f'topics:: {topics}\n'

        with open(fpath, 'w') as f:
            f.write(content)
        print(f"Added topics to {paper_id}: {topics}")

if __name__ == '__main__':
    pub_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'publications')
    add_topics(pub_dir)

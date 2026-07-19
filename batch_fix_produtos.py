#!/usr/bin/env python3
import subprocess, re, sys, os

DIR = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['./batch_json_produtos'], capture_output=True, cwd=DIR)

path = os.path.join(DIR, 'dados/produtos.json')
try:
    with open(path) as f:
        c = f.read()
    c = re.sub(r':\.(\d+)', r':0.\1', c)
    c = re.sub(r',\s+\]', r']', c)
    c = re.sub(r',\s+\}', r'}', c)
    with open(path, 'w') as f:
        f.write(c)
    print('JSON produtos fixed')
except Exception as e:
    print(f'Erro: {e}')

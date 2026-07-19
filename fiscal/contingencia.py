import os
from datetime import datetime

TIPOS_CONTINGENCIA = {
    'normal': 'Normal',
    'scan': 'SCAN - Sistema de Contingencia do Ambiente Nacional',
    'epec': 'EPEC - Evento Previo de Emissao em Contingencia',
    'fsda': 'FS-DA - Formulario de Seguranca',
}

class Contingencia:
    def __init__(self, modo='normal', justificativa='', data_hora=None):
        self.modo = modo
        self.justificativa = justificativa
        self.data_hora = data_hora or datetime.now()

    def ativo(self):
        return self.modo != 'normal'

    def tipo_descricao(self):
        return TIPOS_CONTINGENCIA.get(self.modo, self.modo)

def carregar_contingencia():
    import json
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(DIR, 'dados/contingencia.json')
    try:
        with open(path) as f:
            data = json.load(f)
        return Contingencia(
            modo=data.get('modo', 'normal'),
            justificativa=data.get('justificativa', ''),
        )
    except (FileNotFoundError, json.JSONDecodeError):
        return Contingencia()

def salvar_contingencia(contingencia):
    import json
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(DIR, 'dados/contingencia.json')
    data = {
        'modo': contingencia.modo,
        'justificativa': contingencia.justificativa,
        'data_hora': contingencia.data_hora.isoformat(),
    }
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

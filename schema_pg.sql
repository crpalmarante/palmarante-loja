-- Schema PostgreSQL para consultas e relatorios RH
-- Escrita: COBOL (arquivos .dat) -> Leitura: PostgreSQL

CREATE SCHEMA IF NOT EXISTS rh;

-- Funcionarios (espelho do gerir_funcionarios.cbl)
CREATE TABLE IF NOT EXISTS rh.funcionarios (
    id SERIAL PRIMARY KEY,
    fn_id INTEGER UNIQUE,
    nome VARCHAR(50) NOT NULL,
    usuario VARCHAR(20),
    cpf VARCHAR(14),
    rg VARCHAR(20),
    data_nasc DATE,
    celular VARCHAR(15),
    email VARCHAR(50),
    endereco VARCHAR(80),
    data_admissao DATE,
    data_demissao DATE,
    salario NUMERIC(10,2),
    filial_id INTEGER,
    cargo VARCHAR(50),
    tipo_contrato VARCHAR(20),
    pis VARCHAR(14),
    ctps VARCHAR(15),
    cbo VARCHAR(6),
    grau_instrucao VARCHAR(25),
    banco VARCHAR(30),
    agencia VARCHAR(10),
    conta VARCHAR(15),
    pix VARCHAR(50),
    plano_saude VARCHAR(30),
    vale_transporte DECIMAL(5,2),
    vale_refeicao DECIMAL(7,2),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Dependentes
CREATE TABLE IF NOT EXISTS rh.dependentes (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER REFERENCES rh.funcionarios(fn_id),
    nome VARCHAR(50) NOT NULL,
    parentesco VARCHAR(20),
    data_nasc DATE,
    cpf VARCHAR(14),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Holerites (folha de pagamento)
CREATE TABLE IF NOT EXISTS rh.holerites (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER REFERENCES rh.funcionarios(fn_id),
    competencia VARCHAR(7) NOT NULL, -- MM/AAAA
    tipo VARCHAR(20) DEFAULT 'mensal', -- mensal, ferias, decimo, rescicao
    salario_base NUMERIC(10,2),
    proventos NUMERIC(10,2),
    descontos NUMERIC(10,2),
    liquido NUMERIC(10,2),
    inss NUMERIC(10,2),
    irrf NUMERIC(10,2),
    fgts NUMERIC(10,2),
    horas_extras NUMERIC(10,2),
    faltas NUMERIC(10,2),
    outros_prov NUMERIC(10,2),
    outros_desc NUMERIC(10,2),
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, pago, cancelado
    data_pagamento DATE,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Ponto Eletronico
CREATE TABLE IF NOT EXISTS rh.ponto (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER REFERENCES rh.funcionarios(fn_id),
    data DATE NOT NULL,
    hora_entrada TIME,
    hora_almoco_saida TIME,
    hora_almoco_retorno TIME,
    hora_saida TIME,
    horas_trabalhadas NUMERIC(4,2),
    horas_extras NUMERIC(4,2),
    observacao TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(funcionario_id, data)
);

-- Licencas / Afastamentos
CREATE TABLE IF NOT EXISTS rh.licencas (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER REFERENCES rh.funcionarios(fn_id),
    tipo VARCHAR(30) NOT NULL, -- medica, maternidade, paternidade, ferias, etc
    data_inicio DATE NOT NULL,
    data_fim DATE,
    dias INTEGER,
    motivo TEXT,
    status VARCHAR(20) DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Emprestimos
CREATE TABLE IF NOT EXISTS rh.emprestimos (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER REFERENCES rh.funcionarios(fn_id),
    valor_total NUMERIC(10,2) NOT NULL,
    valor_parcela NUMERIC(10,2),
    parcelas_total INTEGER,
    parcelas_pagas INTEGER DEFAULT 0,
    juros NUMERIC(5,2),
    saldo_devedor NUMERIC(10,2),
    data_solicitacao DATE,
    data_aprovacao DATE,
    status VARCHAR(20) DEFAULT 'rascunho',
    created_at TIMESTAMP DEFAULT NOW()
);

-- View: custo total por funcionario (holerite + beneficios)
CREATE OR REPLACE VIEW rh.vw_custo_funcionario AS
SELECT
    f.fn_id, f.nome, f.cargo, f.filial_id,
    COALESCE(SUM(h.proventos), 0) as total_proventos,
    COALESCE(SUM(h.inss), 0) as total_inss,
    COALESCE(SUM(h.irrf), 0) as total_irrf,
    COALESCE(SUM(h.fgts), 0) as total_fgts,
    COALESCE(SUM(h.liquido), 0) as total_liquido,
    COUNT(h.id) as meses_trabalhados
FROM rh.funcionarios f
LEFT JOIN rh.holerites h ON f.fn_id = h.funcionario_id
WHERE f.ativo = TRUE
GROUP BY f.fn_id, f.nome, f.cargo, f.filial_id;

-- View: dashboard RH
CREATE OR REPLACE VIEW rh.vw_dashboard AS
SELECT
    (SELECT COUNT(*) FROM rh.funcionarios WHERE ativo = TRUE) as total_funcionarios,
    (SELECT COUNT(*) FROM rh.funcionarios WHERE ativo = FALSE) as total_desligados,
    (SELECT COUNT(*) FROM rh.licencas WHERE status = 'aprovado' AND CURRENT_DATE BETWEEN data_inicio AND COALESCE(data_fim, CURRENT_DATE)) as em_licenca,
    (SELECT COALESCE(SUM(liquido), 0) FROM rh.holerites WHERE competencia = TO_CHAR(CURRENT_DATE, 'MM/YYYY')) as folha_mes_atual,
    (SELECT COALESCE(SUM(inss), 0) FROM rh.holerites WHERE competencia = TO_CHAR(CURRENT_DATE, 'MM/YYYY')) as inss_mes,
    (SELECT COALESCE(SUM(irrf), 0) FROM rh.holerites WHERE competencia = TO_CHAR(CURRENT_DATE, 'MM/YYYY')) as irrf_mes,
    (SELECT COALESCE(SUM(fgts), 0) FROM rh.holerites WHERE competencia = TO_CHAR(CURRENT_DATE, 'MM/YYYY')) as fgts_mes;

-- Indices
CREATE INDEX IF NOT EXISTS idx_holerites_funcionario ON rh.holerites(funcionario_id);
CREATE INDEX IF NOT EXISTS idx_holerites_competencia ON rh.holerites(competencia);
CREATE INDEX IF NOT EXISTS idx_ponto_funcionario_data ON rh.ponto(funcionario_id, data);
CREATE INDEX IF NOT EXISTS idx_licencas_funcionario ON rh.licencas(funcionario_id);
CREATE INDEX IF NOT EXISTS idx_emprestimos_funcionario ON rh.emprestimos(funcionario_id);

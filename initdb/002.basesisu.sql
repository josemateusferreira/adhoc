-- script_tables.sql

CREATE TABLE IF NOT EXISTS public.curso (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.edicoes (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    ano INTEGER,
    semestre INTEGER CHECK (semestre IN (1,2)),
    data_inicio DATE,
    data_fim DATE
);

CREATE TABLE IF NOT EXISTS public.edicao_curso (
    id SERIAL PRIMARY KEY,
    edicao_id INTEGER NOT NULL REFERENCES edicoes(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES curso(id),
    vagas_ac INTEGER DEFAULT 0,
    vagas_ppi_br INTEGER DEFAULT 0,
    vagas_publica_br INTEGER DEFAULT 0,
    vagas_ppi_publica INTEGER DEFAULT 0,
    vagas_publica INTEGER DEFAULT 0,
    vagas_deficientes INTEGER DEFAULT 0,
    UNIQUE(edicao_id, curso_id)
);

CREATE TABLE IF NOT EXISTS public.candidato (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento DATE,
    categoria TEXT,
    curso_id INTEGER REFERENCES curso(id),
    nota FLOAT
);

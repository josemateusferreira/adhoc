INSERT INTO curso (nome) VALUES ('Engenharia');
INSERT INTO curso (nome) VALUES ('Ciência da Computação');

-- Inserir duas edições de SISU
INSERT INTO edicoes (nome, ano, semestre, data_inicio, data_fim) VALUES
	('SISU ' || 2025 || '.1', 2025, 1, '2025-01-15', '2025-02-15'),
	('SISU ' || 2025 || '.2', 2025, 2, '2025-07-01', '2025-07-30');

-- Associar cursos às edições
-- Engenharia e Ciência da Computação para ambas as edições
INSERT INTO edicao_curso (edicao_id, curso_id, vagas_ac, vagas_ppi_br, vagas_publica_br, vagas_ppi_publica, vagas_publica, vagas_deficientes) VALUES
	(1, 1, 10, 2, 3, 1, 2, 1),
	(1, 2, 15, 3, 4, 2, 3, 2),
	(2, 1, 12, 2, 3, 1, 2, 1),
	(2, 2, 18, 4, 5, 2, 4, 2);

INSERT INTO candidato (nome, cpf, data_nascimento, categoria, edicao_curso_id, nota) VALUES
    ('João Silva', '12345678901', '2000-05-10', 'AC', 1, 750.5),
    ('Maria Souza', '23456789012', '1999-08-22', 'PPI BR', 2, 800.0),
    ('Carlos Lima', '34567890123', '2001-03-15', 'Pública BR', 3, 720.0),
    ('Ana Costa', '45678901234', '2002-11-30', 'AC', 4, 780.0),
    ('Bruno Martins', '56789012345', '2001-09-12', 'PPI Pública', 1, 765.0),
    ('Fernanda Alves', '67890123456', '2000-02-28', 'Deficientes', 2, 710.0),
    ('Lucas Pereira', '78901234567', '1998-12-05', 'AC', 3, 805.5),
    ('Patrícia Ramos', '89012345678', '2003-04-17', 'Pública', 4, 695.0),
    ('Gabriel Torres', '90123456789', '2002-07-23', 'PPI BR', 1, 780.0),
    ('Juliana Rocha', '01234567890', '2001-10-30', 'AC', 2, 820.0);


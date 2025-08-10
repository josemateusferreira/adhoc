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
('Juliana Rocha', '01234567890', '2001-10-30', 'AC', 2, 820.0),
('Ricardo Nunes', '11111111111', '2000-06-14', 'AC', 1, 845.0),
('Camila Duarte', '22222222222', '1999-03-22', 'PPI BR', 2, 812.5),
('Eduardo Mendes', '33333333333', '2001-12-11', 'Pública BR', 3, 790.0),
('Vanessa Araújo', '44444444444', '2000-01-07', 'Deficientes', 4, 705.0),
('Tiago Souza', '55555555555', '2002-08-25', 'PPI Pública', 1, 755.0),
('Renata Barros', '66666666666', '2003-05-19', 'Pública', 2, 678.0),
('Marcos Teixeira', '77777777777', '1998-09-30', 'AC', 3, 810.0),
('Sofia Ribeiro', '88888888888', '2001-11-03', 'PPI BR', 4, 832.0),
('Felipe Gomes', '99999999999', '2002-04-29', 'AC', 1, 799.0),
('Larissa Melo', '10101010101', '2000-07-13', 'Pública BR', 2, 715.0),
('André Batista', '12121212121', '1999-10-01', 'PPI Pública', 3, 765.5),
('Beatriz Ferreira', '13131313131', '2001-02-08', 'Deficientes', 4, 702.0),
('Diego Almeida', '14141414141', '2000-12-19', 'AC', 1, 885.0),
('Carolina Monteiro', '15151515151', '1998-05-16', 'PPI BR', 2, 845.5),
('Fábio Cardoso', '16161616161', '2001-06-24', 'Pública BR', 3, 775.0),
('Natália Lopes', '17171717171', '2002-03-05', 'Pública', 4, 690.0),
('Pedro Henrique', '18181818181', '2000-09-09', 'AC', 1, 820.0),
('Isabela Martins', '19191919191', '1999-01-21', 'PPI Pública', 2, 765.0),
('Rafael Santana', '20202020202', '2001-08-15', 'Deficientes', 3, 715.5),
('Aline Oliveira', '21212121212', '2003-10-10', 'Pública', 4, 698.0),
('Gustavo Rocha', '22232323232', '2000-11-25', 'AC', 1, 880.0),
('Luana Silva', '23242424242', '1999-04-17', 'PPI BR', 2, 835.0),
('Matheus Lima', '24252525252', '2001-07-07', 'Pública BR', 3, 760.0),
('Bruna Almeida', '25262626262', '2002-02-14', 'Deficientes', 4, 705.5),
('Caio Mendes', '26272727272', '2000-05-23', 'AC', 1, 830.0),
('Daniela Costa', '27282828282', '1998-06-18', 'PPI Pública', 2, 745.0),
('Thiago Fernandes', '28292929292', '2001-01-01', 'Pública', 3, 710.0),
('Paula Souza', '29303030303', '2002-08-08', 'Pública', 4, 692.0);



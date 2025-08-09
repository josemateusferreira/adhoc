-- Inserir duas edições de SISU
INSERT INTO edicoes (nome, ano, semestre, data_inicio, data_fim) VALUES
  ('SISU 2025/1', 2025, 1, '2025-01-15', '2025-02-15'),
  ('SISU 2025/2', 2025, 2, '2025-07-01', '2025-07-30');

-- Associar cursos às edições
-- Engenharia e Ciência da Computação para ambas as edições
INSERT INTO edicao_curso (edicao_id, curso_id, vagas_ac, vagas_ppi_br, vagas_publica_br, vagas_ppi_publica, vagas_publica, vagas_deficientes) VALUES
  (1, 1, 10, 2, 3, 1, 2, 1),
  (1, 2, 15, 3, 4, 2, 3, 2),
  (2, 1, 12, 2, 3, 1, 2, 1),
  (2, 2, 18, 4, 5, 2, 4, 2);

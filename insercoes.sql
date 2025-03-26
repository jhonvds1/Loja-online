INSERT INTO Produto (nome, preco, categoria) VALUES 
('Camiseta Básica Masculina', 49.90, 'Camisetas'),
('Vestido Longo Feminino', 179.90, 'Vestidos'),
('Calça Jeans Skinny', 119.90, 'Calças'),
('Jaqueta de Couro Masculina', 299.90, 'Jaquetas'),
('Blusa de Tricot Feminina', 89.90, 'Blusas'),
('Tênis Esportivo Feminino', 159.90, 'Tênis'),
('Saia Midi Floral', 89.90, 'Saídas de Praia'),
('Shorts Jeans Feminino', 59.90, 'Shorts'),
('Camisa Polo Masculina', 89.90, 'Camisetas'),
('Bermuda Masculina Casual', 69.90, 'Shorts');

INSERT INTO Cliente (nome, email, senha_hash, rua, numero, bairro, cidade, estado) VALUES
('Ana Silva', 'ana.silva@gmail.com', 'hashAna', 'Rua das Flores', '100', 'Centro', 'São Paulo', 'SP'),
('Carlos Souza', 'carlos.souza@yahoo.com', 'hashCarlos', 'Av. Paulista', '234', 'Bela Vista', 'São Paulo', 'SP'),
('Mariana Oliveira', 'mariana.oliveira@hotmail.com', 'hashMariana', 'Rua dos Três Irmãos', '567', 'Morumbi', 'São Paulo', 'SP'),
('Lucas Mendes', 'lucas.mendes@outlook.com', 'hashLucas', 'Av. Rio Branco', '890', 'Centro', 'Rio de Janeiro', 'RJ'),
('Juliana Santos', 'juliana.santos@gmail.com', 'hashJuliana', 'Rua da Paz', '123', 'Jardim América', 'Curitiba', 'PR'),
('Fernanda Lima', 'fernanda.lima@yahoo.com', 'hashFernanda', 'Rua do Sol', '345', 'Jardim Europa', 'Porto Alegre', 'RS'),
('João Pereira', 'joao.pereira@hotmail.com', 'hashJoao', 'Rua das Palmeiras', '678', 'Itaim Bibi', 'São Paulo', 'SP'),
('Larissa Costa', 'larissa.costa@outlook.com', 'hashLarissa', 'Rua das Acácias', '987', 'Vila Madalena', 'São Paulo', 'SP'),
('Ricardo Alves', 'ricardo.alves@gmail.com', 'hashRicardo', 'Av. Brasil', '432', 'Zona Norte', 'Rio de Janeiro', 'RJ'),
('Beatriz Rocha', 'beatriz.rocha@yahoo.com', 'hashBeatriz', 'Rua da Liberdade', '765', 'Zona Leste', 'São Paulo', 'SP');

INSERT INTO Compra (ID_Cliente, Valor_Total, Status, Data_Compra) VALUES
(1, 179.90, 'Pago', CURRENT_TIMESTAMP),
(2, 119.90, 'Aguardando Pagamento', CURRENT_TIMESTAMP),
(3, 89.90, 'Pago', CURRENT_TIMESTAMP),
(4, 299.90, 'Cancelado', CURRENT_TIMESTAMP),
(5, 159.90, 'Pago', CURRENT_TIMESTAMP),
(6, 89.90, 'Aguardando Pagamento', CURRENT_TIMESTAMP),
(7, 69.90, 'Pago', CURRENT_TIMESTAMP),
(8, 59.90, 'Pago', CURRENT_TIMESTAMP),
(9, 119.90, 'Cancelado', CURRENT_TIMESTAMP),
(10, 89.90, 'Aguardando Pagamento', CURRENT_TIMESTAMP);

INSERT INTO Carrinho (ID_Cliente) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Item_Carrinho (ID_Carrinho, ID_Produto, quantidade) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 3, 1),
(3, 4, 1),
(4, 5, 3),
(5, 6, 1),
(6, 7, 2),
(7, 8, 1),
(8, 9, 2),
(9, 10, 1);

INSERT INTO Item_Compra (ID_Compra, ID_Produto, Quantidade, Preco) VALUES
(1, 1, 1, 49.90),
(2, 2, 1, 179.90),
(3, 3, 2, 89.90),
(4, 4, 1, 299.90),
(5, 5, 3, 159.90),
(6, 6, 1, 89.90),
(7, 7, 2, 69.90),
(8, 8, 1, 59.90),
(9, 9, 1, 119.90),
(10, 10, 1, 89.90);

INSERT INTO Avaliacao (ID_Cliente, nota, comentario) VALUES
(1, 5, 'Ótima qualidade e conforto!'),
(2, 4, 'Bom produto, mas o tecido poderia ser melhor.'),
(3, 5, 'Adorei, recomendo!'),
(4, 2, 'Não gostei do corte do vestido.'),
(5, 5, 'Muito confortável, adorei!'),
(6, 3, 'O modelo não é o que eu esperava.'),
(7, 4, 'Bonito, mas o caimento não ficou perfeito.'),
(8, 5, 'Perfeito, tudo como eu queria!'),
(9, 3, 'O produto chegou com defeito.'),
(10, 4, 'Bom, mas o tecido poderia ser melhor.');

INSERT INTO Estoque (quantidade) VALUES
(150), (120), (180), (100), (220), (140), (160), (190), (130), (110);

INSERT INTO Fornecedor (CNPJ, Email, Telefone, Nome) VALUES
('12345678000195', 'fornecedor1@loja.com', '(11) 99999-9999', 'Fornecedor A'),
('23456789000186', 'fornecedor2@loja.com', '(21) 88888-8888', 'Fornecedor B'),
('34567890000177', 'fornecedor3@loja.com', '(31) 77777-7777', 'Fornecedor C');

INSERT INTO Fornece (ID_Produto, CNPJ) VALUES
(1, '12345678000195'),
(2, '23456789000186'),
(3, '34567890000177'),
(4, '12345678000195'),
(5, '23456789000186'),
(6, '34567890000177'),
(7, '12345678000195'),
(8, '23456789000186'),
(9, '34567890000177'),
(10, '12345678000195');

INSERT INTO Devolucao_Troca (Tipo, Status, Data_Solicitacao, Motivo, ID_cliente) 
VALUES
('Troca', 'Aguardando Avaliação', '2025-03-22 10:30:00', 'Produto com defeito', 1),
('Devolução', 'Aguardando Avaliação', '2025-03-21 14:00:00', 'Produto não atende às expectativas', 2),
('Troca', 'Aguardando Avaliação', '2025-03-20 09:15:00', 'Tamanho errado', 3),
('Devolução', 'Aguardando Avaliação', '2025-03-19 16:20:00', 'Produto diferente do anunciado', 4),
('Troca', 'Aguardando Avaliação', '2025-03-18 11:00:00', 'Cor não corresponde', 5),
('Devolução', 'Aguardando Avaliação', '2025-03-17 12:45:00', 'Produto danificado', 6),
('Troca', 'Aguardando Avaliação', '2025-03-16 13:30:00', 'Tamanho não adequado', 7),
('Devolução', 'Aguardando Avaliação', '2025-03-15 15:00:00', 'Produto com defeito de fabricação', 8),
('Troca', 'Aguardando Avaliação', '2025-03-14 10:00:00', 'Produto não combina com a roupa', 9),
('Devolução', 'Aguardando Avaliação', '2025-03-13 17:30:00', 'Erro na entrega do produto', 10);

INSERT INTO Recebe (AvaliacaoID, ID_Produto) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Solicita (ID_Compra, ID_Troca) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Devolvido_Trocado (ID_Troca, ID_Produto) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Vendido_Em (ID_Produto) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Inclui (ID_Compra) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Tem_Em (ID_Produto, ID_Estoque) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Adicionado (ID_Produto) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Contem_Itens (ID_Carrinho) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO Solicita_Reposicao (ID_Estoque, CNPJ, quantidade, data_pedido, status) VALUES
(1, '12345678000195', 20, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(2, '23456789000186', 30, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(3, '34567890000177', 25, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(4, '12345678000195', 15, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(5, '23456789000186', 40, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(6, '34567890000177', 35, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(7, '12345678000195', 22, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(8, '23456789000186', 28, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(9, '34567890000177', 18, CURRENT_TIMESTAMP, 'Aguardando Confirmação'),
(10, '12345678000195', 32, CURRENT_TIMESTAMP, 'Aguardando Confirmação');



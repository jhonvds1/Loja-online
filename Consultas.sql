--Consultar quais clientes compraram mais que determinado valor
select cl.nome , co.valor_total from cliente cl
join compra co on cl.id_cliente = co.id_cliente
where valor_total>150

--Consultar a nota e o comentário de cada produto
select pr.nome , av.nota, av.comentario
from produto pr
join recebe re on pr.id_produto=re.id_produto
join avaliacao av on av.id_avaliacao = re.avaliacaoid;

--Consultar quais clientes pediram para trocar ou devolver produtos e o motivo
select cl.nome , pr.nome , dt.motivo from cliente cl
join devolucao_troca dt on dt.id_cliente=cl.id_cliente
join devolvido_trocado de_tro on dt.id_troca=de_tro.id_troca
join produto pr on pr.id_produto=de_tro.id_produto;

--Consultar o que cada cliente comprou, o valor e a quantidade
select cl.nome as nome_cliente , pr.nome as nome_produto , pr.preco , ic.quantidade
from produto pr
join adicionado ad on ad.id_produto = pr.id_produto
join item_carrinho ic on ic.id_produto = ad.id_produto
join contem_itens ci on ic.id_carrinho = ci.id_carrinho
join carrinho c on c.id_carrinho = ci.id_carrinho
join cliente cl on cl.id_cliente = c.id_cliente;

--Consultar a quantidade em estoque de cada produto
select pr.nome , e.quantidade 
from produto pr 
join tem_em te on pr.id_produto = te.id_produto
join estoque e on e.id_estoque = te.id_produto

--Consultar o que cada fornecedor fornece
select fo.nome , fo.cnpj , fo.telefone , pr.nome
from produto pr
join fornece fn on fn.id_produto = pr.id_produto
join fornecedor fo on fo.cnpj = fn.cnpj



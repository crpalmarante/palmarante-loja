.PHONY: all compilar dados produtos venda relatorios json serve clean pg deploy

all: compilar dados

compilar:
	cobc -x -free gerar_produtos.cbl -o gerar_produtos
	cobc -x -free cadastrar_produto.cbl -o cadastrar_produto
	cobc -x -free registrar_venda.cbl -o registrar_venda
	cobc -x -free relatorios.cbl -o relatorios
	cobc -x -free batch_json_produtos.cbl -o batch_json_produtos
	cobc -x -free batch_json_vendas.cbl -o batch_json_vendas
	cobc -x -free gerir_empresa.cbl -o gerir_empresa
	cobc -x -free gerir_filiais.cbl -o gerir_filiais
	cobc -x -free gerir_funcionarios.cbl -o gerir_funcionarios
	cobc -x -free gerir_usuarios.cbl -o gerir_usuarios
	cobc -x -free gerir_atributos.cbl -o gerir_atributos
	cobc -x -free gerir_imagens.cbl -o gerir_imagens
	cobc -x -free finalizar_pedido.cbl -o finalizar_pedido
	cobc -x -free gerir_numeracao.cbl -o gerir_numeracao
	cobc -x -free gerir_fornecedores.cbl -o gerir_fornecedores
	cobc -x -free batch_json_fornecedores.cbl -o batch_json_fornecedores
	cobc -x -free batch_json_numeracao.cbl -o batch_json_numeracao
	cobc -x -free categoria_disciplinar.cbl -o categoria_disciplinar
	cobc -x -free acao_disciplinar.cbl -o acao_disciplinar
	cobc -x -free licenca.cbl -o licenca
	cobc -x -free timesheet.cbl -o timesheet
	cobc -x -free emprestimo.cbl -o emprestimo
	cobc -x -free dependentes.cbl -o dependentes
	cobc -x -free ponto.cbl -o ponto

dados: compilar
	./gerar_produtos

json: dados
	./batch_fix_produtos.py 2>/dev/null
	./batch_json_vendas 2>/dev/null
	./batch_json_fornecedores 2>/dev/null
	./batch_json_numeracao 2>/dev/null

relatorio: dados
	./relatorios

serve:
	python3 server.py

deploy:
	@if [ "$(shell id -u)" -ne 0 ]; then echo "Execute com sudo: sudo make deploy"; exit 1; fi
	@bash deploy.sh "$(PWD)"

clean:
	rm -f gerar_produtos cadastrar_produto registrar_venda relatorios
	rm -f batch_json_produtos batch_json_vendas gerir_empresa gerir_filiais
	rm -f gerir_funcionarios gerir_usuarios gerir_atributos gerir_imagens finalizar_pedido gerir_numeracao gerir_fornecedores batch_json_fornecedores batch_json_numeracao categoria_disciplinar acao_disciplinar licenca timesheet emprestimo
	rm -f dados/*.dat dados/*.json
	rm -f *.json sync_pg.sql

       >>SOURCE FORMAT IS FREE
       *> gerar_produtos.cbl - Gera dados iniciais de produtos e vendas
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerarProdutos.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT vendas-file ASSIGN TO "dados/vendas.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT itens-file ASSIGN TO "dados/itens_venda.dat"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD prod-file.
       01 prod-reg.
           05 pr-id              PIC 9(6).
           05 pr-nome            PIC X(50).
           05 pr-preco           PIC 9(7)V99.
           05 pr-preco-custo     PIC 9(7)V99.
           05 pr-stock           PIC 9(6).
           05 pr-margem          PIC 9(3)V99.
           05 pr-ativo           PIC X(1).
           05 pr-codigo-barras   PIC X(14).
            05 pr-categoria       PIC X(20).
            05 pr-sub-categoria   PIC X(20).
            05 pr-unidade         PIC X(4).
           05 pr-ncm             PIC X(8).
            05 pr-fornecedor      PIC X(30).
            05 pr-localizacao     PIC X(15).
             05 pr-filial-id       PIC 9(3).
             05 pr-cst            PIC X(3).
             05 pr-cfop           PIC X(4).
             05 pr-icms-alq       PIC 9(3)V99.
             05 pr-servico        PIC X(1).
             05 pr-iss-alq        PIC 9(3)V99.
             05 pr-cod-serv-mun   PIC X(20).

        FD vendas-file.
       01 venda-reg.
           05 vd-id          PIC 9(6).
           05 vd-data        PIC X(10).
           05 vd-hora        PIC X(8).
           05 vd-cliente     PIC X(50).
           05 vd-total       PIC 9(9)V99.
            05 vd-forma-pg    PIC X(15).
            05 vd-filial-id       PIC 9(3).

        FD itens-file.
       01 item-reg.
           05 iv-venda-id    PIC 9(6).
           05 iv-item        PIC 9(3).
           05 iv-prod-id     PIC 9(6).
           05 iv-prod-nome   PIC X(50).
           05 iv-qtd         PIC 9(4).
           05 iv-preco-uni   PIC 9(7)V99.
            05 iv-subtotal    PIC 9(9)V99.
            05 iv-filial-id       PIC 9(3).

        PROCEDURE DIVISION.
           PERFORM gerar-produtos
           PERFORM gerar-vendas
           STOP RUN.

        gerar-produtos.
            OPEN OUTPUT prod-file

             MOVE 0 TO pr-filial-id
             MOVE "400" TO pr-cst
             MOVE "6102" TO pr-cfop
             MOVE 18.00 TO pr-icms-alq
             MOVE "N" TO pr-servico
             MOVE 0 TO pr-iss-alq
             MOVE SPACES TO pr-cod-serv-mun
             MOVE 1 TO pr-id MOVE "Arroz 5kg" TO pr-nome
           MOVE 32.90 TO pr-preco MOVE 28.50 TO pr-preco-custo
           MOVE 50 TO pr-stock MOVE 15.45 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560011" TO pr-codigo-barras
            MOVE "Alimentacao" TO pr-categoria
            MOVE "Graos" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "1906.10.00" TO pr-ncm
            MOVE "Fornecedor A" TO pr-fornecedor
            MOVE "A1-01" TO pr-localizacao
            WRITE prod-reg

            MOVE 2 TO pr-id MOVE "Feijao 1kg" TO pr-nome
           MOVE 15.90 TO pr-preco MOVE 12.00 TO pr-preco-custo
           MOVE 80 TO pr-stock MOVE 32.50 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560028" TO pr-codigo-barras
            MOVE "Alimentacao" TO pr-categoria
            MOVE "Graos" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "0713.33.00" TO pr-ncm
            MOVE "Fornecedor A" TO pr-fornecedor
            MOVE "A1-02" TO pr-localizacao
            WRITE prod-reg

            MOVE 3 TO pr-id MOVE "Oleo de Soja 900ml" TO pr-nome
           MOVE 12.40 TO pr-preco MOVE 9.80 TO pr-preco-custo
           MOVE 60 TO pr-stock MOVE 26.53 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560035" TO pr-codigo-barras
            MOVE "Alimentacao" TO pr-categoria
            MOVE "Oleos" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "1507.10.00" TO pr-ncm
            MOVE "Fornecedor B" TO pr-fornecedor
            MOVE "A1-03" TO pr-localizacao
            WRITE prod-reg

            MOVE 4 TO pr-id MOVE "Acucar 2kg" TO pr-nome
           MOVE 8.90 TO pr-preco MOVE 6.50 TO pr-preco-custo
           MOVE 40 TO pr-stock MOVE 36.92 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560042" TO pr-codigo-barras
            MOVE "Alimentacao" TO pr-categoria
            MOVE "Acucares" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "1701.14.00" TO pr-ncm
            MOVE "Fornecedor A" TO pr-fornecedor
            MOVE "A1-04" TO pr-localizacao
            WRITE prod-reg

            MOVE 5 TO pr-id MOVE "Cafe 500g" TO pr-nome
           MOVE 18.90 TO pr-preco MOVE 14.20 TO pr-preco-custo
           MOVE 30 TO pr-stock MOVE 33.10 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560059" TO pr-codigo-barras
            MOVE "Alimentacao" TO pr-categoria
            MOVE "Cafes" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "0901.21.00" TO pr-ncm
            MOVE "Fornecedor C" TO pr-fornecedor
            MOVE "A2-01" TO pr-localizacao
            WRITE prod-reg

            MOVE 6 TO pr-id MOVE "Leite 1L" TO pr-nome
           MOVE 6.50 TO pr-preco MOVE 4.80 TO pr-preco-custo
           MOVE 100 TO pr-stock MOVE 35.38 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560066" TO pr-codigo-barras
            MOVE "Bebidas" TO pr-categoria
            MOVE "Leites" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "0401.10.00" TO pr-ncm
            MOVE "Fornecedor B" TO pr-fornecedor
            MOVE "A2-02" TO pr-localizacao
            WRITE prod-reg

            MOVE 7 TO pr-id MOVE "Paozinho" TO pr-nome
           MOVE 3.50 TO pr-preco MOVE 2.10 TO pr-preco-custo
           MOVE 200 TO pr-stock MOVE 66.67 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560073" TO pr-codigo-barras
            MOVE "Padaria" TO pr-categoria
            MOVE "Paes" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "1905.90.00" TO pr-ncm
            MOVE "Fornecedor D" TO pr-fornecedor
            MOVE "B1-01" TO pr-localizacao
            WRITE prod-reg

            MOVE 8 TO pr-id MOVE "Refrigerante 2L" TO pr-nome
           MOVE 9.80 TO pr-preco MOVE 6.90 TO pr-preco-custo
           MOVE 45 TO pr-stock MOVE 42.03 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560080" TO pr-codigo-barras
            MOVE "Bebidas" TO pr-categoria
            MOVE "Refrigerantes" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "2202.10.00" TO pr-ncm
            MOVE "Fornecedor B" TO pr-fornecedor
            MOVE "B1-02" TO pr-localizacao
            WRITE prod-reg

            MOVE 9 TO pr-id MOVE "Sabao em po 1kg" TO pr-nome
           MOVE 14.50 TO pr-preco MOVE 10.80 TO pr-preco-custo
           MOVE 35 TO pr-stock MOVE 34.26 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560097" TO pr-codigo-barras
            MOVE "Limpeza" TO pr-categoria
            MOVE "Saboes" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "3402.20.00" TO pr-ncm
            MOVE "Fornecedor E" TO pr-fornecedor
            MOVE "C1-01" TO pr-localizacao
            WRITE prod-reg

            MOVE 10 TO pr-id MOVE "Detergente 500ml" TO pr-nome
           MOVE 4.20 TO pr-preco MOVE 2.90 TO pr-preco-custo
           MOVE 90 TO pr-stock MOVE 44.83 TO pr-margem MOVE "S" TO pr-ativo
           MOVE "7891234560103" TO pr-codigo-barras
            MOVE "Limpeza" TO pr-categoria
            MOVE "Detergentes" TO pr-sub-categoria
            MOVE "UN" TO pr-unidade MOVE "3402.20.00" TO pr-ncm
            MOVE "Fornecedor E" TO pr-fornecedor
            MOVE "C1-02" TO pr-localizacao
            WRITE prod-reg

            CLOSE prod-file
           DISPLAY "10 produtos gerados em dados/produtos.dat".

       gerar-vendas.
           OPEN OUTPUT vendas-file
           OPEN OUTPUT itens-file

            MOVE 0 TO vd-filial-id
            MOVE 1 TO vd-id
            MOVE "2026-07-12" TO vd-data MOVE "09:15:00" TO vd-hora
            MOVE "Cliente A" TO vd-cliente MOVE 65.80 TO vd-total
            MOVE "Dinheiro" TO vd-forma-pg
            WRITE venda-reg

            MOVE 0 TO iv-filial-id
            MOVE 1 TO iv-venda-id MOVE 1 TO iv-item
            MOVE 1 TO iv-prod-id MOVE "Arroz 5kg" TO iv-prod-nome
            MOVE 2 TO iv-qtd MOVE 32.90 TO iv-preco-uni MOVE 65.80 TO iv-subtotal
            WRITE item-reg

            MOVE 0 TO vd-filial-id
            MOVE 2 TO vd-id
           MOVE "2026-07-12" TO vd-data MOVE "14:30:00" TO vd-hora
           MOVE "Cliente B" TO vd-cliente MOVE 37.80 TO vd-total
           MOVE "Cartao" TO vd-forma-pg
           WRITE venda-reg

            MOVE 0 TO iv-filial-id
            MOVE 2 TO iv-venda-id MOVE 1 TO iv-item
            MOVE 5 TO iv-prod-id MOVE "Cafe 500g" TO iv-prod-nome
            MOVE 1 TO iv-qtd MOVE 18.90 TO iv-preco-uni MOVE 18.90 TO iv-subtotal
            WRITE item-reg
            MOVE 0 TO iv-filial-id
            MOVE 2 TO iv-venda-id MOVE 2 TO iv-item
           MOVE 7 TO iv-prod-id MOVE "Paozinho" TO iv-prod-nome
           MOVE 3 TO iv-qtd MOVE 3.50 TO iv-preco-uni MOVE 10.50 TO iv-subtotal
           WRITE item-reg
            MOVE 0 TO iv-filial-id
            MOVE 2 TO iv-venda-id MOVE 3 TO iv-item
            MOVE 10 TO iv-prod-id MOVE "Detergente 500ml" TO iv-prod-nome
            MOVE 2 TO iv-qtd MOVE 4.20 TO iv-preco-uni MOVE 8.40 TO iv-subtotal
            WRITE item-reg

            MOVE 0 TO vd-filial-id
            MOVE 3 TO vd-id
           MOVE "2026-07-12" TO vd-data MOVE "18:00:00" TO vd-hora
           MOVE "Cliente C" TO vd-cliente MOVE 9.80 TO vd-total
           MOVE "PIX" TO vd-forma-pg
           WRITE venda-reg

            MOVE 0 TO iv-filial-id
            MOVE 3 TO iv-venda-id MOVE 1 TO iv-item
            MOVE 8 TO iv-prod-id MOVE "Refrigerante 2L" TO iv-prod-nome
            MOVE 1 TO iv-qtd MOVE 9.80 TO iv-preco-uni MOVE 9.80 TO iv-subtotal
            WRITE item-reg

           CLOSE vendas-file
           CLOSE itens-file
           DISPLAY "3 vendas geradas em dados/vendas.dat".

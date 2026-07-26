       >>SOURCE FORMAT IS FREE
       *> relatorios.cbl - Relatorios do POS
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Relatorios.

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


        WORKING-STORAGE SECTION.
        01 ws-total-vendas    PIC 9(9)V99.
        01 ws-total-prod      PIC 9(9)V99.
        01 ws-qtd-vendas      PIC 9(6).
        01 ws-qtd-itens       PIC 9(6).
        01 ws-count           PIC 9(6).
        01 ws-valor           PIC 9(9)V99.
        01 ws-id-anterior     PIC 9(6).
        01 ws-primeiro        PIC X(1).
        01 ws-prod-id-ant     PIC 9(6).
        01 ws-qtd-prod        PIC 9(6).
        01 ws-valor-prod      PIC 9(9)V99.
        01 ws-qtd-alim        PIC 9(6).
        01 ws-qtd-beb         PIC 9(6).
        01 ws-qtd-lim         PIC 9(6).
        01 ws-qtd-pad         PIC 9(6).

       PROCEDURE DIVISION.
            DISPLAY "========== RELATORIOS POS =========="
            PERFORM resumo-dia
            PERFORM vendas-por-forma
            PERFORM top-produtos
            PERFORM produtos-baixo-stock
            PERFORM stock-por-categoria
            STOP RUN.

       resumo-dia.
           DISPLAY "--- Resumo do Dia ---"
           MOVE 0 TO ws-qtd-vendas ws-total-vendas ws-qtd-itens
           OPEN INPUT vendas-file
           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-qtd-vendas
               ADD vd-total TO ws-total-vendas
           END-PERFORM
           CLOSE vendas-file

           OPEN INPUT itens-file
           PERFORM UNTIL 1 = 2
               READ itens-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD iv-qtd TO ws-qtd-itens
           END-PERFORM
           CLOSE itens-file

           DISPLAY "Vendas: " ws-qtd-vendas
           DISPLAY "Itens vendidos: " ws-qtd-itens
           DISPLAY "Facturado: R$ " ws-total-vendas.

       vendas-por-forma.
           DISPLAY "--- Vendas por Forma de Pagamento ---"
           MOVE 0 TO ws-count ws-valor
           MOVE "S" TO ws-primeiro
           MOVE SPACES TO vd-forma-pg

           OPEN INPUT vendas-file
           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF ws-primeiro = "S" THEN
                   MOVE vd-forma-pg TO vd-forma-pg
                   MOVE "N" TO ws-primeiro
               END-IF
           END-PERFORM
           CLOSE vendas-file

           OPEN INPUT vendas-file
           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD vd-total TO ws-valor
               ADD 1 TO ws-count
           END-PERFORM
           CLOSE vendas-file
           DISPLAY "Total: " ws-count " vendas | R$ " ws-valor.

       top-produtos.
           DISPLAY "--- Top Produtos Mais Vendidos ---"
           MOVE 0 TO ws-prod-id-ant ws-qtd-prod ws-valor-prod
           MOVE "S" TO ws-primeiro

           OPEN INPUT itens-file
           PERFORM UNTIL 1 = 2
               READ itens-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               DISPLAY iv-prod-id " | "
                   FUNCTION TRIM(iv-prod-nome) " | "
                   iv-qtd "x | R$ " iv-subtotal
           END-PERFORM
           CLOSE itens-file.

       produtos-baixo-stock.
           DISPLAY "--- Produtos com Stock Baixo (< 10) ---"
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-ativo = "S" AND pr-stock < 10 THEN
                   DISPLAY pr-id " | " FUNCTION TRIM(pr-nome)
                       " | Stock: " pr-stock
               END-IF
           END-PERFORM
            CLOSE prod-file.

       stock-por-categoria.
           DISPLAY "--- Stock por Categoria ---"
           MOVE 0 TO ws-qtd-alim ws-qtd-beb ws-qtd-lim ws-qtd-pad
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-ativo = "S" THEN
                   EVALUATE pr-categoria
                       WHEN "Alimentacao" ADD pr-stock TO ws-qtd-alim
                       WHEN "Bebidas"     ADD pr-stock TO ws-qtd-beb
                       WHEN "Limpeza"     ADD pr-stock TO ws-qtd-lim
                       WHEN "Padaria"     ADD pr-stock TO ws-qtd-pad
                   END-EVALUATE
               END-IF
           END-PERFORM
           CLOSE prod-file
           DISPLAY "Alimentacao: " ws-qtd-alim " unidades"
           DISPLAY "Bebidas:     " ws-qtd-beb " unidades"
           DISPLAY "Limpeza:     " ws-qtd-lim " unidades"
           DISPLAY "Padaria:     " ws-qtd-pad " unidades".

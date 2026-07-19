       >>SOURCE FORMAT IS FREE
       *> registrar_venda.cbl - Registra venda e baixa stock
       *> Uso: CLIENTE=... FORMA_PG=...
       *>       ITEM_1_PROD=1 ITEM_1_QTD=2
       *>       ITEM_2_PROD=5 ITEM_2_QTD=1 ...
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RegistrarVenda.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT temp-file ASSIGN TO "dados/produtos.tmp"
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

        FD temp-file.
        01 temp-reg.
            05 tr-id              PIC 9(6).
            05 tr-nome            PIC X(50).
            05 tr-preco           PIC 9(7)V99.
            05 tr-preco-custo     PIC 9(7)V99.
            05 tr-stock           PIC 9(6).
            05 tr-margem          PIC 9(3)V99.
            05 tr-ativo           PIC X(1).
            05 tr-codigo-barras   PIC X(14).
            05 tr-categoria       PIC X(20).
            05 tr-sub-categoria   PIC X(20).
            05 tr-unidade         PIC X(4).
           05 tr-ncm             PIC X(8).
           05 tr-fornecedor      PIC X(30).
            05 tr-localizacao     PIC X(15).
            05 tr-filial-id       PIC 9(3).

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
       01 ws-cliente         PIC X(50).
       01 ws-forma-pg        PIC X(15).
       01 ws-prod-id         PIC 9(6).
       01 ws-qtd             PIC 9(4).
       01 ws-qtd-in          PIC X(6).
       01 ws-prod-encontrado PIC X(1).
       01 ws-stock-insuf     PIC X(1).
       01 ws-erro            PIC X(1).
       01 ws-msg-erro        PIC X(100).
       01 ws-prox-venda      PIC 9(6).
       01 ws-prox-item       PIC 9(3).
       01 ws-total           PIC 9(9)V99.
       01 ws-subtotal        PIC 9(9)V99.
       01 ws-preco-uni       PIC 9(7)V99.
       01 ws-nome-prod       PIC X(50).
       01 ws-i               PIC 9(2).
       01 ws-i-ed            PIC Z9.
       01 ws-param           PIC X(20).
       01 ws-valor           PIC X(50).
        01 ws-data            PIC X(10).
        01 ws-hora            PIC X(8).
        01 ws-filial-id       PIC 9(3).
        01 ws-filial-id-in    PIC X(5).
        01 ws-desconto        PIC 9(3).
        01 ws-desconto-in     PIC X(6).
        01 ws-tipo            PIC X(1).
        01 ws-tipo-in         PIC X(5).

        PROCEDURE DIVISION.
           PERFORM ler-dados-venda
           IF ws-erro = "S" THEN DISPLAY "ERRO:" ws-msg-erro STOP RUN END-IF
           PERFORM processar-itens
           IF ws-erro = "S" THEN DISPLAY "ERRO:" ws-msg-erro STOP RUN END-IF
           PERFORM registrar
           DISPLAY "VENDA_OK:" ws-prox-venda " Total:R$" ws-total
           STOP RUN.

       ler-dados-venda.
           MOVE "N" TO ws-erro
           ACCEPT ws-cliente FROM ENVIRONMENT "CLIENTE"
           IF ws-cliente = SPACES THEN MOVE "Consumidor" TO ws-cliente END-IF
           ACCEPT ws-forma-pg FROM ENVIRONMENT "FORMA_PG"
            IF ws-forma-pg = SPACES THEN
                MOVE "ERRO: forma de pagamento obrigatoria" TO ws-msg-erro
                MOVE "S" TO ws-erro
            END-IF
            ACCEPT ws-filial-id-in FROM ENVIRONMENT "FILIAL_ID"
            IF ws-filial-id-in NOT = SPACES THEN
                COMPUTE ws-filial-id = FUNCTION NUMVAL(ws-filial-id-in)
            ELSE MOVE 0 TO ws-filial-id END-IF.

       processar-itens.
           MOVE 0 TO ws-prox-item
           MOVE 0 TO ws-total
           MOVE "N" TO ws-stock-insuf

           PERFORM VARYING ws-i FROM 1 BY 1 UNTIL ws-i > 20
               MOVE ws-i TO ws-i-ed
               INITIALIZE ws-param
               STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_PROD" INTO ws-param
               ACCEPT ws-valor FROM ENVIRONMENT FUNCTION TRIM(ws-param)
               IF ws-valor = SPACES THEN EXIT PERFORM END-IF
               COMPUTE ws-prod-id = FUNCTION NUMVAL(ws-valor)

               MOVE ws-i TO ws-i-ed
               INITIALIZE ws-param
               STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_QTD" INTO ws-param
               ACCEPT ws-valor FROM ENVIRONMENT FUNCTION TRIM(ws-param)
                COMPUTE ws-qtd = FUNCTION NUMVAL(ws-valor)
                IF ws-qtd = 0 THEN MOVE 1 TO ws-qtd END-IF

                MOVE ws-i TO ws-i-ed
                INITIALIZE ws-param
                STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_DESC" INTO ws-param
                ACCEPT ws-desconto-in FROM ENVIRONMENT FUNCTION TRIM(ws-param)
                IF ws-desconto-in NOT = SPACES THEN
                    COMPUTE ws-desconto = FUNCTION NUMVAL(ws-desconto-in)
                ELSE MOVE 0 TO ws-desconto END-IF

                PERFORM buscar-produto
               IF ws-prod-encontrado = "N" THEN
                   STRING "produto " ws-prod-id " nao encontrado"
                       INTO ws-msg-erro
                   MOVE "S" TO ws-erro
                   EXIT PERFORM
               END-IF

                IF ws-desconto > 0 THEN
                    COMPUTE ws-preco-uni = ws-preco-uni *
                        (100 - ws-desconto) / 100
                END-IF

                IF ws-stock-insuf = "N" THEN
                    PERFORM baixar-stock
                END-IF
                ADD 1 TO ws-prox-item
                COMPUTE ws-subtotal = ws-qtd * ws-preco-uni
               ADD ws-subtotal TO ws-total
           END-PERFORM

           IF ws-prox-item = 0 THEN
               MOVE "nenhum item na venda" TO ws-msg-erro
               MOVE "S" TO ws-erro
           END-IF.

       buscar-produto.
           MOVE "N" TO ws-prod-encontrado
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id = ws-prod-id AND pr-ativo = "S" THEN
                   MOVE "S" TO ws-prod-encontrado
                   MOVE pr-preco TO ws-preco-uni
                   MOVE pr-nome TO ws-nome-prod
                   IF pr-stock < ws-qtd THEN
                       MOVE "S" TO ws-stock-insuf
                       STRING "stock insuficiente para " FUNCTION TRIM(pr-nome)
                           INTO ws-msg-erro
                   END-IF
               END-IF
           END-PERFORM
           CLOSE prod-file.

       baixar-stock.
           OPEN INPUT prod-file
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id = ws-prod-id THEN
                   SUBTRACT ws-qtd FROM pr-stock
               END-IF
                MOVE pr-id TO tr-id MOVE pr-nome TO tr-nome
                MOVE pr-preco TO tr-preco
                MOVE pr-preco-custo TO tr-preco-custo
                MOVE pr-stock TO tr-stock MOVE pr-margem TO tr-margem
                MOVE pr-ativo TO tr-ativo
                MOVE pr-codigo-barras TO tr-codigo-barras
                MOVE pr-categoria TO tr-categoria
                MOVE pr-sub-categoria TO tr-sub-categoria
                MOVE pr-unidade TO tr-unidade MOVE pr-ncm TO tr-ncm
                MOVE pr-fornecedor TO tr-fornecedor
                MOVE pr-localizacao TO tr-localizacao
                MOVE pr-filial-id TO tr-filial-id
                WRITE temp-reg
           END-PERFORM
           CLOSE prod-file
           CLOSE temp-file
           CALL "system" USING "mv dados/produtos.tmp dados/produtos.dat"
           END-CALL.

       registrar.
           MOVE 0 TO ws-prox-venda
           OPEN INPUT vendas-file
           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF vd-id > ws-prox-venda THEN MOVE vd-id TO ws-prox-venda END-IF
            END-PERFORM
            CLOSE vendas-file
            ADD 1 TO ws-prox-venda

            ACCEPT ws-tipo-in FROM ENVIRONMENT "TIPO"
            IF ws-tipo-in NOT = SPACES THEN
                MOVE ws-tipo-in TO ws-tipo
                IF ws-tipo = "O" THEN MOVE "ORCAMENTO" TO ws-forma-pg END-IF
                IF ws-tipo = "P" THEN MOVE "PENDENTE" TO ws-forma-pg END-IF
            END-IF

            ACCEPT ws-data FROM ENVIRONMENT "DATA_VENDA"
           IF ws-data = SPACES THEN
               STRING FUNCTION CURRENT-DATE(1:4) "-"
                      FUNCTION CURRENT-DATE(5:2) "-"
                      FUNCTION CURRENT-DATE(7:2)
                   INTO ws-data
               END-STRING
           END-IF
           ACCEPT ws-hora FROM ENVIRONMENT "HORA_VENDA"
           IF ws-hora = SPACES THEN
               STRING FUNCTION CURRENT-DATE(9:2) ":"
                      FUNCTION CURRENT-DATE(11:2) ":"
                      FUNCTION CURRENT-DATE(13:2)
                   INTO ws-hora
               END-STRING
           END-IF

           OPEN EXTEND vendas-file
           MOVE ws-prox-venda TO vd-id
           MOVE ws-data TO vd-data
           MOVE ws-hora TO vd-hora
            MOVE ws-cliente TO vd-cliente
            MOVE ws-total TO vd-total
            MOVE ws-forma-pg TO vd-forma-pg
            MOVE ws-filial-id TO vd-filial-id
            WRITE venda-reg
            CLOSE vendas-file

           OPEN EXTEND itens-file
           PERFORM VARYING ws-i FROM 1 BY 1 UNTIL ws-i > ws-prox-item
               MOVE ws-i TO ws-i-ed
               INITIALIZE ws-param
               STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_PROD" INTO ws-param
               ACCEPT ws-valor FROM ENVIRONMENT FUNCTION TRIM(ws-param)
               COMPUTE ws-prod-id = FUNCTION NUMVAL(ws-valor)
               MOVE ws-i TO ws-i-ed
               INITIALIZE ws-param
               STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_QTD" INTO ws-param
               ACCEPT ws-valor FROM ENVIRONMENT FUNCTION TRIM(ws-param)
                COMPUTE ws-qtd = FUNCTION NUMVAL(ws-valor)

                MOVE ws-i TO ws-i-ed
                INITIALIZE ws-param
                STRING "ITEM_" FUNCTION TRIM(ws-i-ed) "_DESC" INTO ws-param
                ACCEPT ws-desconto-in FROM ENVIRONMENT FUNCTION TRIM(ws-param)
                IF ws-desconto-in NOT = SPACES THEN
                    COMPUTE ws-desconto = FUNCTION NUMVAL(ws-desconto-in)
                ELSE MOVE 0 TO ws-desconto END-IF

                PERFORM buscar-produto-read
                IF ws-desconto > 0 THEN
                    COMPUTE ws-preco-uni = ws-preco-uni *
                        (100 - ws-desconto) / 100
                END-IF
                MOVE ws-prox-venda TO iv-venda-id
               MOVE ws-i TO iv-item
               MOVE ws-prod-id TO iv-prod-id
               MOVE ws-nome-prod TO iv-prod-nome
               MOVE ws-qtd TO iv-qtd
               MOVE ws-preco-uni TO iv-preco-uni
               COMPUTE ws-subtotal = ws-qtd * ws-preco-uni
                MOVE ws-subtotal TO iv-subtotal
                MOVE ws-filial-id TO iv-filial-id
                WRITE item-reg
           END-PERFORM
           CLOSE itens-file.

       buscar-produto-read.
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id = ws-prod-id THEN
                   MOVE pr-preco TO ws-preco-uni
                   MOVE pr-nome TO ws-nome-prod
               END-IF
           END-PERFORM
           CLOSE prod-file.

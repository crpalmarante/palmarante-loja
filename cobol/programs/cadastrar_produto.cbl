       >>SOURCE FORMAT IS FREE
       *> cadastrar_produto.cbl - CRUD de produtos via ambiente
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CadastrarProduto.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT temp-file ASSIGN TO "dados/produtos.tmp"
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
             05 tr-cst            PIC X(3).
             05 tr-cfop           PIC X(4).
              05 tr-icms-alq       PIC 9(3)V99.
              05 tr-servico        PIC X(1).
              05 tr-iss-alq        PIC 9(3)V99.
              05 tr-cod-serv-mun   PIC X(20).

        WORKING-STORAGE SECTION.
        01 ws-acao            PIC X(15).
       01 ws-id              PIC 9(6).
       01 ws-nome            PIC X(50).
       01 ws-preco           PIC 9(7)V99.
       01 ws-preco-in        PIC X(15).
       01 ws-preco-custo     PIC 9(7)V99.
       01 ws-custo-in        PIC X(15).
       01 ws-stock           PIC 9(6).
       01 ws-stock-in        PIC X(10).
       01 ws-margem          PIC 9(3)V99.
       01 ws-margem-in       PIC X(10).
       01 ws-codigo-barras   PIC X(14).
        01 ws-categoria       PIC X(20).
        01 ws-sub-categoria   PIC X(20).
        01 ws-unidade         PIC X(4).
       01 ws-ncm             PIC X(8).
       01 ws-fornecedor      PIC X(30).
        01 ws-localizacao     PIC X(15).
         01 ws-filial-id       PIC 9(3).
         01 ws-filial-id-in    PIC X(5).
         01 ws-cst             PIC X(3).
         01 ws-cfop            PIC X(4).
         01 ws-icms-alq        PIC 9(3)V99.
          01 ws-icms-in         PIC X(10).
          01 ws-servico         PIC X(1).
          01 ws-iss-alq         PIC 9(3)V99.
          01 ws-iss-in          PIC X(10).
          01 ws-cod-serv-mun    PIC X(20).
          01 ws-encontrou       PIC X(1).
       01 ws-prox-id         PIC 9(6).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "alterar"  PERFORM alterar
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-preco-in FROM ENVIRONMENT "PRECO"
           ACCEPT ws-custo-in FROM ENVIRONMENT "PRECO_CUSTO"
           ACCEPT ws-stock-in FROM ENVIRONMENT "STOCK"
           ACCEPT ws-margem-in FROM ENVIRONMENT "MARGEM"
           ACCEPT ws-codigo-barras FROM ENVIRONMENT "CODIGO_BARRAS"
            ACCEPT ws-categoria FROM ENVIRONMENT "CATEGORIA"
            ACCEPT ws-sub-categoria FROM ENVIRONMENT "SUB_CATEGORIA"
            ACCEPT ws-unidade FROM ENVIRONMENT "UNIDADE"
            ACCEPT ws-ncm FROM ENVIRONMENT "NCM"
             ACCEPT ws-fornecedor FROM ENVIRONMENT "FORNECEDOR"
             ACCEPT ws-localizacao FROM ENVIRONMENT "LOCALIZACAO"
              ACCEPT ws-filial-id-in FROM ENVIRONMENT "FILIAL_ID"
               IF ws-filial-id-in NOT = SPACES THEN
                   COMPUTE ws-filial-id = FUNCTION NUMVAL(ws-filial-id-in)
               ELSE MOVE 0 TO ws-filial-id END-IF
              ACCEPT ws-cst FROM ENVIRONMENT "CST"
              ACCEPT ws-cfop FROM ENVIRONMENT "CFOP"
               ACCEPT ws-icms-in FROM ENVIRONMENT "ICMS_ALQ"
               IF ws-icms-in NOT = SPACES THEN
                   COMPUTE ws-icms-alq = FUNCTION NUMVAL(ws-icms-in) END-IF
               ACCEPT ws-servico FROM ENVIRONMENT "SERVICO"
               ACCEPT ws-iss-in FROM ENVIRONMENT "ISS_ALQ"
               IF ws-iss-in NOT = SPACES THEN
                   COMPUTE ws-iss-alq = FUNCTION NUMVAL(ws-iss-in) END-IF
               ACCEPT ws-cod-serv-mun FROM ENVIRONMENT "COD_SERV_MUN"


               IF ws-nome = SPACES THEN
                 DISPLAY "ERRO: nome obrigatorio" STOP RUN END-IF
             IF ws-categoria = SPACES THEN
                DISPLAY "ERRO: categoria obrigatoria" STOP RUN END-IF
            IF ws-sub-categoria = SPACES THEN
                DISPLAY "ERRO: sub-categoria obrigatoria" STOP RUN END-IF

           IF ws-preco-in NOT = SPACES THEN
               COMPUTE ws-preco = FUNCTION NUMVAL(ws-preco-in) END-IF
           IF ws-custo-in NOT = SPACES THEN
               COMPUTE ws-preco-custo = FUNCTION NUMVAL(ws-custo-in) END-IF
           IF ws-stock-in NOT = SPACES THEN
               COMPUTE ws-stock = FUNCTION NUMVAL(ws-stock-in) END-IF
           IF ws-margem-in NOT = SPACES THEN
               COMPUTE ws-margem = FUNCTION NUMVAL(ws-margem-in) END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id > ws-prox-id THEN MOVE pr-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE prod-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND prod-file
           MOVE ws-prox-id TO pr-id
           MOVE ws-nome TO pr-nome
           MOVE ws-preco TO pr-preco
           MOVE ws-preco-custo TO pr-preco-custo
           MOVE ws-stock TO pr-stock
           MOVE ws-margem TO pr-margem
           MOVE "S" TO pr-ativo
           MOVE ws-codigo-barras TO pr-codigo-barras
            MOVE ws-categoria TO pr-categoria
            MOVE ws-sub-categoria TO pr-sub-categoria
            MOVE ws-unidade TO pr-unidade
           MOVE ws-ncm TO pr-ncm
            MOVE ws-fornecedor TO pr-fornecedor
            MOVE ws-localizacao TO pr-localizacao
             MOVE ws-filial-id TO pr-filial-id
             MOVE ws-cst TO pr-cst
             MOVE ws-cfop TO pr-cfop
             MOVE ws-icms-alq TO pr-icms-alq
             MOVE ws-servico TO pr-servico
             MOVE ws-iss-alq TO pr-iss-alq
             MOVE ws-cod-serv-mun TO pr-cod-serv-mun
             WRITE prod-reg
            CLOSE prod-file
            DISPLAY ws-prox-id.

       alterar.
            ACCEPT ws-id FROM ENVIRONMENT "ID"
            ACCEPT ws-nome FROM ENVIRONMENT "NOME"
            ACCEPT ws-preco-in FROM ENVIRONMENT "PRECO"
            ACCEPT ws-custo-in FROM ENVIRONMENT "PRECO_CUSTO"
            ACCEPT ws-stock-in FROM ENVIRONMENT "STOCK"
            ACCEPT ws-margem-in FROM ENVIRONMENT "MARGEM"
            ACCEPT ws-codigo-barras FROM ENVIRONMENT "CODIGO_BARRAS"
            ACCEPT ws-categoria FROM ENVIRONMENT "CATEGORIA"
            ACCEPT ws-sub-categoria FROM ENVIRONMENT "SUB_CATEGORIA"
            ACCEPT ws-unidade FROM ENVIRONMENT "UNIDADE"
            ACCEPT ws-ncm FROM ENVIRONMENT "NCM"
             ACCEPT ws-fornecedor FROM ENVIRONMENT "FORNECEDOR"
             ACCEPT ws-localizacao FROM ENVIRONMENT "LOCALIZACAO"
              ACCEPT ws-filial-id-in FROM ENVIRONMENT "FILIAL_ID"
               IF ws-filial-id-in NOT = SPACES THEN
                   COMPUTE ws-filial-id = FUNCTION NUMVAL(ws-filial-id-in)
               ELSE MOVE 0 TO ws-filial-id END-IF
              ACCEPT ws-cst FROM ENVIRONMENT "CST"
              ACCEPT ws-cfop FROM ENVIRONMENT "CFOP"
               ACCEPT ws-icms-in FROM ENVIRONMENT "ICMS_ALQ"
               IF ws-icms-in NOT = SPACES THEN
                   COMPUTE ws-icms-alq = FUNCTION NUMVAL(ws-icms-in) END-IF
               ACCEPT ws-servico FROM ENVIRONMENT "SERVICO"
               ACCEPT ws-iss-in FROM ENVIRONMENT "ISS_ALQ"
               IF ws-iss-in NOT = SPACES THEN
                   COMPUTE ws-iss-alq = FUNCTION NUMVAL(ws-iss-in) END-IF
               ACCEPT ws-cod-serv-mun FROM ENVIRONMENT "COD_SERV_MUN"


              IF ws-preco-in NOT = SPACES THEN
               COMPUTE ws-preco = FUNCTION NUMVAL(ws-preco-in) END-IF
           IF ws-custo-in NOT = SPACES THEN
               COMPUTE ws-preco-custo = FUNCTION NUMVAL(ws-custo-in) END-IF
           IF ws-stock-in NOT = SPACES THEN
               COMPUTE ws-stock = FUNCTION NUMVAL(ws-stock-in) END-IF
           IF ws-margem-in NOT = SPACES THEN
               COMPUTE ws-margem = FUNCTION NUMVAL(ws-margem-in) END-IF

           MOVE "N" TO ws-encontrou
           OPEN INPUT prod-file
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN MOVE ws-nome TO pr-nome END-IF
                   IF ws-preco-in NOT = SPACES THEN
                       MOVE ws-preco TO pr-preco END-IF
                   IF ws-custo-in NOT = SPACES THEN
                       MOVE ws-preco-custo TO pr-preco-custo END-IF
                   IF ws-stock-in NOT = SPACES THEN
                       MOVE ws-stock TO pr-stock END-IF
                   IF ws-margem-in NOT = SPACES THEN
                       MOVE ws-margem TO pr-margem END-IF
                   IF ws-codigo-barras NOT = SPACES THEN
                       MOVE ws-codigo-barras TO pr-codigo-barras END-IF
                    IF ws-categoria NOT = SPACES THEN
                        MOVE ws-categoria TO pr-categoria END-IF
                    IF ws-sub-categoria NOT = SPACES THEN
                        MOVE ws-sub-categoria TO pr-sub-categoria END-IF
                    IF ws-unidade NOT = SPACES THEN
                       MOVE ws-unidade TO pr-unidade END-IF
                   IF ws-ncm NOT = SPACES THEN
                       MOVE ws-ncm TO pr-ncm END-IF
                   IF ws-fornecedor NOT = SPACES THEN
                       MOVE ws-fornecedor TO pr-fornecedor END-IF
                    IF ws-localizacao NOT = SPACES THEN
                        MOVE ws-localizacao TO pr-localizacao END-IF
                     IF ws-filial-id-in NOT = SPACES THEN
                         MOVE ws-filial-id TO pr-filial-id END-IF
                     IF ws-cst NOT = SPACES THEN
                         MOVE ws-cst TO pr-cst END-IF
                     IF ws-cfop NOT = SPACES THEN
                         MOVE ws-cfop TO pr-cfop END-IF
                     IF ws-icms-in NOT = SPACES THEN
                          MOVE ws-icms-alq TO pr-icms-alq END-IF
                      IF ws-servico NOT = SPACES THEN
                          MOVE ws-servico TO pr-servico END-IF
                      IF ws-iss-in NOT = SPACES THEN
                          MOVE ws-iss-alq TO pr-iss-alq END-IF
                      IF ws-cod-serv-mun NOT = SPACES THEN
                          MOVE ws-cod-serv-mun TO pr-cod-serv-mun END-IF
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
                 MOVE pr-cst TO tr-cst
                 MOVE pr-cfop TO tr-cfop
                  MOVE pr-icms-alq TO tr-icms-alq
                  MOVE pr-servico TO tr-servico
                  MOVE pr-iss-alq TO tr-iss-alq
                  MOVE pr-cod-serv-mun TO tr-cod-serv-mun
                  WRITE temp-reg
            END-PERFORM
           CLOSE prod-file CLOSE temp-file
           CALL "system" USING "mv dados/produtos.tmp dados/produtos.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: produto nao encontrado".

       excluir.
           ACCEPT ws-id FROM ENVIRONMENT "ID"
           MOVE "N" TO ws-encontrou
           OPEN INPUT prod-file
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-id NOT = ws-id THEN
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
                     MOVE pr-cst TO tr-cst
                     MOVE pr-cfop TO tr-cfop
                      MOVE pr-icms-alq TO tr-icms-alq
                      MOVE pr-servico TO tr-servico
                      MOVE pr-iss-alq TO tr-iss-alq
                      MOVE pr-cod-serv-mun TO tr-cod-serv-mun
                      WRITE temp-reg
                ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE prod-file CLOSE temp-file
           CALL "system" USING "mv dados/produtos.tmp dados/produtos.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: produto nao encontrado".

       listar.
           OPEN INPUT prod-file
           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF pr-ativo = "S" THEN
                   DISPLAY pr-id " | " FUNCTION TRIM(pr-nome)
                       " | " pr-preco " | " pr-stock
               END-IF
           END-PERFORM
           CLOSE prod-file.

       >>SOURCE FORMAT IS FREE
       *> gerir_atributos.cbl - CRUD de atributos de produtos
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirAtributos.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT at-file ASSIGN TO "dados/atributos.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/atributos.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-prod-status.

       DATA DIVISION.
       FILE SECTION.
       FD at-file.
       01 at-reg.
           05 at-id          PIC 9(6).
           05 at-produto-id  PIC 9(6).
           05 at-nome        PIC X(30).
           05 at-valor       PIC X(30).

       FD temp-file.
       01 temp-reg.
           05 tl-id          PIC 9(6).
           05 tl-produto-id  PIC 9(6).
           05 tl-nome        PIC X(30).
           05 tl-valor       PIC X(30).

       FD prod-file.
       01 prod-reg.
           05 pr-id          PIC 9(6).
           05 pr-nome        PIC X(50).
           05 pr-preco       PIC 9(7)V99.
           05 pr-preco-custo PIC 9(7)V99.
           05 pr-stock       PIC 9(6).
           05 pr-margem      PIC 9(3)V99.
           05 pr-ativo       PIC X.
           05 pr-codigo-barras PIC X(14).
           05 pr-categoria   PIC X(20).
           05 pr-sub-categoria PIC X(20).
           05 pr-unidade     PIC X(4).
           05 pr-ncm         PIC X(8).
           05 pr-fornecedor  PIC X(30).
           05 pr-localizacao PIC X(15).
           05 pr-filial-id   PIC 9(3).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-prod-status     PIC X(2).
       01 ws-encontrou       PIC X(1).
       01 ws-json-linha      PIC X(500).
       01 ws-id-ed           PIC Z(6)9.
       01 ws-prod-id-ed      PIC Z(6)9.
       01 ws-total-ed        PIC ZZZ9.
       01 ws-id              PIC 9(6).
       01 ws-produto-id      PIC 9(6).
       01 ws-produto-id-in   PIC X(10).
       01 ws-id-in           PIC X(10).
       01 ws-nome            PIC X(30).
       01 ws-valor           PIC X(30).
       01 ws-prox-id         PIC 9(6).
       01 ws-qtd             PIC 9(4).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "alterar"  PERFORM alterar
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN "listar-por-produto" PERFORM listar-por-produto
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

        incluir.
            ACCEPT ws-produto-id-in FROM ENVIRONMENT "PRODUTO_ID"
            COMPUTE ws-produto-id = FUNCTION NUMVAL(ws-produto-id-in)
            ACCEPT ws-nome FROM ENVIRONMENT "NOME"
            ACCEPT ws-valor FROM ENVIRONMENT "VALOR"
            IF ws-nome = SPACES THEN
                DISPLAY "ERRO: nome do atributo obrigatorio" STOP RUN END-IF
            IF ws-produto-id = 0 THEN
                DISPLAY "ERRO: produto_id obrigatorio" STOP RUN END-IF

            MOVE "N" TO ws-encontrou
            OPEN INPUT prod-file
            IF ws-prod-status NOT = "35" THEN
                PERFORM UNTIL 1 = 2
                    READ prod-file NEXT RECORD
                        AT END EXIT PERFORM
                    END-READ
                    IF pr-id = ws-produto-id AND pr-ativo = "S" THEN
                        MOVE "S" TO ws-encontrou
                        EXIT PERFORM
                    END-IF
                END-PERFORM
            END-IF
            CLOSE prod-file
            IF ws-encontrou = "N" THEN
                DISPLAY "ERRO: produto nao encontrado" STOP RUN END-IF

            MOVE 0 TO ws-prox-id
           OPEN INPUT at-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT at-file CLOSE at-file
               OPEN INPUT at-file END-IF
           PERFORM UNTIL 1 = 2
               READ at-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF at-id > ws-prox-id THEN MOVE at-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE at-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND at-file
           MOVE ws-prox-id TO at-id
           MOVE ws-produto-id TO at-produto-id
           MOVE ws-nome TO at-nome
           MOVE ws-valor TO at-valor
           WRITE at-reg
           CLOSE at-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-valor FROM ENVIRONMENT "VALOR"

           MOVE "N" TO ws-encontrou
           OPEN INPUT at-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: atributo nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ at-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF at-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN MOVE ws-nome TO at-nome END-IF
                   IF ws-valor NOT = SPACES THEN MOVE ws-valor TO at-valor END-IF
               END-IF
               MOVE at-id TO tl-id
               MOVE at-produto-id TO tl-produto-id
               MOVE at-nome TO tl-nome
               MOVE at-valor TO tl-valor
               WRITE temp-reg
           END-PERFORM
           CLOSE at-file CLOSE temp-file
           CALL "system" USING "mv dados/atributos.tmp dados/atributos.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: atributo nao encontrado".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT at-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: atributo nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ at-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF at-id NOT = ws-id THEN
                   MOVE at-id TO tl-id
                   MOVE at-produto-id TO tl-produto-id
                   MOVE at-nome TO tl-nome
                   MOVE at-valor TO tl-valor
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE at-file CLOSE temp-file
           CALL "system" USING "mv dados/atributos.tmp dados/atributos.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: atributo nao encontrado".

       listar.
           OPEN INPUT at-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"atributos":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"atributos":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-prox-id
           PERFORM UNTIL 1 = 2
               READ at-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-prox-id
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE at-id TO ws-id-ed
               MOVE at-produto-id TO ws-prod-id-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"produto_id":' FUNCTION TRIM(ws-prod-id-ed)
                      ',"nome":"' FUNCTION TRIM(at-nome) '"'
                      ',"valor":"' FUNCTION TRIM(at-valor) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-prox-id TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE at-file.

       listar-por-produto.
           ACCEPT ws-produto-id-in FROM ENVIRONMENT "PRODUTO_ID"
           COMPUTE ws-produto-id = FUNCTION NUMVAL(ws-produto-id-in)

           OPEN INPUT at-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"atributos":[],"total":0}'
               STOP RUN END-IF
           MOVE 0 TO ws-qtd
           DISPLAY '{"atributos":['
           MOVE "S" TO ws-encontrou
           PERFORM UNTIL 1 = 2
               READ at-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF at-produto-id = ws-produto-id THEN
                   ADD 1 TO ws-qtd
                   IF ws-encontrou = "S" THEN
                       MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE at-id TO ws-id-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"nome":"' FUNCTION TRIM(at-nome) '"'
                          ',"valor":"' FUNCTION TRIM(at-valor) '"}'
                       INTO ws-json-linha
                   DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-qtd TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE at-file.

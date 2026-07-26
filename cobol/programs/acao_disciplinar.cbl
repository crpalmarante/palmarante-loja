       >>SOURCE FORMAT IS FREE
       *> acao_disciplinar.cbl - CRUD de acoes disciplinares
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AcaoDisciplinar.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT acao-file ASSIGN TO "dados/acoes_disciplinares.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/acoes_disciplinares.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD acao-file.
       01 acao-reg.
           05 ac-id                PIC 9(4).
           05 ac-funcionario-id    PIC 9(3).
           05 ac-categoria-id      PIC 9(4).
           05 ac-data              PIC X(10).
           05 ac-descricao         PIC X(200).
           05 ac-dias-desconto     PIC 9(3).
           05 ac-valor-desconto    PIC 9(7)V99.
           05 ac-status            PIC X(1).

       FD temp-file.
       01 temp-reg.
           05 tl-id                PIC 9(4).
           05 tl-funcionario-id    PIC 9(3).
           05 tl-categoria-id      PIC 9(4).
           05 tl-data              PIC X(10).
           05 tl-descricao         PIC X(200).
           05 tl-dias-desconto     PIC 9(3).
           05 tl-valor-desconto    PIC 9(7)V99.
           05 tl-status            PIC X(1).

       WORKING-STORAGE SECTION.
       01 ws-acao           PIC X(20).
       01 ws-file-status    PIC X(2).
       01 ws-encontrou      PIC X.
       01 ws-prox-id        PIC 9(4).
       01 ws-total          PIC 9(4).
       01 ws-total-ed       PIC Z(3)9.
       01 ws-id-ed          PIC Z(3)9.
       01 ws-id-in          PIC X(5).
       01 ws-id             PIC 9(4).
       01 ws-func-id        PIC 9(3).
       01 ws-func-id-ed     PIC Z(3)9.
       01 ws-func-id-in     PIC X(5).
       01 ws-cat-id         PIC 9(4).
       01 ws-cat-id-ed      PIC Z(3)9.
       01 ws-cat-id-in      PIC X(5).
       01 ws-data           PIC X(10).
       01 ws-descricao      PIC X(200).
       01 ws-dias-in        PIC X(5).
       01 ws-dias           PIC 9(3).
       01 ws-valor-in       PIC X(12).
       01 ws-valor          PIC 9(7)V99.
       01 ws-valor-ed       PIC Z(6)9.99.
       01 ws-dias-ed        PIC Z(3)9.
       01 ws-status         PIC X(1).
       01 ws-json-linha     PIC X(600).

       PROCEDURE DIVISION.

           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"        PERFORM incluir
               WHEN "alterar"        PERFORM alterar
               WHEN "excluir"        PERFORM excluir
               WHEN "listar"         PERFORM listar
               WHEN "listar-por-func" PERFORM listar-por-func
               WHEN OTHER            DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-cat-id-in FROM ENVIRONMENT "CATEGORIA_ID"
           COMPUTE ws-cat-id = FUNCTION NUMVAL(ws-cat-id-in)
           ACCEPT ws-data FROM ENVIRONMENT "DATA"
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS_DESCONTO"
           COMPUTE ws-dias = FUNCTION NUMVAL(ws-dias-in)
           ACCEPT ws-valor-in FROM ENVIRONMENT "VALOR_DESCONTO"
           COMPUTE ws-valor = FUNCTION NUMVAL(ws-valor-in)
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"
           IF ws-status = SPACES THEN MOVE "A" TO ws-status END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT acao-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT acao-file CLOSE acao-file
               OPEN INPUT acao-file END-IF
           PERFORM UNTIL 1 = 2
               READ acao-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF ac-id > ws-prox-id THEN MOVE ac-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE acao-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND acao-file
           MOVE ws-prox-id TO ac-id
           MOVE ws-func-id TO ac-funcionario-id
           MOVE ws-cat-id TO ac-categoria-id
           MOVE ws-data TO ac-data
           MOVE ws-descricao TO ac-descricao
           MOVE ws-dias TO ac-dias-desconto
           MOVE ws-valor TO ac-valor-desconto
           MOVE ws-status TO ac-status
           WRITE acao-reg
           CLOSE acao-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           IF ws-func-id-in NOT = SPACES THEN
               COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in) END-IF
           ACCEPT ws-cat-id-in FROM ENVIRONMENT "CATEGORIA_ID"
           IF ws-cat-id-in NOT = SPACES THEN
               COMPUTE ws-cat-id = FUNCTION NUMVAL(ws-cat-id-in) END-IF
           ACCEPT ws-data FROM ENVIRONMENT "DATA"
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS_DESCONTO"
           IF ws-dias-in NOT = SPACES THEN
               COMPUTE ws-dias = FUNCTION NUMVAL(ws-dias-in) END-IF
           ACCEPT ws-valor-in FROM ENVIRONMENT "VALOR_DESCONTO"
           IF ws-valor-in NOT = SPACES THEN
               COMPUTE ws-valor = FUNCTION NUMVAL(ws-valor-in) END-IF
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"

           MOVE "N" TO ws-encontrou
           OPEN INPUT acao-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ acao-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF ac-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-func-id-in NOT = SPACES THEN
                       MOVE ws-func-id TO ac-funcionario-id END-IF
                   IF ws-cat-id-in NOT = SPACES THEN
                       MOVE ws-cat-id TO ac-categoria-id END-IF
                   IF ws-data NOT = SPACES THEN
                       MOVE ws-data TO ac-data END-IF
                   IF ws-descricao NOT = SPACES THEN
                       MOVE ws-descricao TO ac-descricao END-IF
                   IF ws-dias-in NOT = SPACES THEN
                       MOVE ws-dias TO ac-dias-desconto END-IF
                   IF ws-valor-in NOT = SPACES THEN
                       MOVE ws-valor TO ac-valor-desconto END-IF
                   IF ws-status NOT = SPACES THEN
                       MOVE ws-status TO ac-status END-IF
               END-IF
               MOVE ac-id TO tl-id
               MOVE ac-funcionario-id TO tl-funcionario-id
               MOVE ac-categoria-id TO tl-categoria-id
               MOVE ac-data TO tl-data
               MOVE ac-descricao TO tl-descricao
               MOVE ac-dias-desconto TO tl-dias-desconto
               MOVE ac-valor-desconto TO tl-valor-desconto
               MOVE ac-status TO tl-status
               WRITE temp-reg
           END-PERFORM
           CLOSE acao-file CLOSE temp-file
           CALL "system" USING "mv dados/acoes_disciplinares.tmp dados/acoes_disciplinares.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT acao-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ acao-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF ac-id NOT = ws-id THEN
                   MOVE ac-id TO tl-id
                   MOVE ac-funcionario-id TO tl-funcionario-id
                   MOVE ac-categoria-id TO tl-categoria-id
                   MOVE ac-data TO tl-data
                   MOVE ac-descricao TO tl-descricao
                   MOVE ac-dias-desconto TO tl-dias-desconto
                   MOVE ac-valor-desconto TO tl-valor-desconto
                   MOVE ac-status TO tl-status
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE acao-file CLOSE temp-file
           CALL "system" USING "mv dados/acoes_disciplinares.tmp dados/acoes_disciplinares.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       listar.
           OPEN INPUT acao-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"acoes":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"acoes":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ acao-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE ac-id TO ws-id-ed
               MOVE ac-funcionario-id TO ws-func-id-ed
               MOVE ac-categoria-id TO ws-cat-id-ed
               MOVE ac-valor-desconto TO ws-valor-ed
               MOVE ac-dias-desconto TO ws-dias-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                      ',"categoria_id":' FUNCTION TRIM(ws-cat-id-ed)
                      ',"data":"' FUNCTION TRIM(ac-data) '"'
                      ',"descricao":"' FUNCTION TRIM(ac-descricao) '"'
                      ',"dias_desconto":' FUNCTION TRIM(ws-dias-ed)
                      ',"valor_desconto":' FUNCTION TRIM(ws-valor-ed)
                      ',"status":"' FUNCTION TRIM(ac-status) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE acao-file.

       listar-por-func.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)

           OPEN INPUT acao-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"acoes":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"acoes":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ acao-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF ac-funcionario-id = ws-func-id THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN
                       MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE ac-id TO ws-id-ed
                   MOVE ac-funcionario-id TO ws-func-id-ed
                   MOVE ac-categoria-id TO ws-cat-id-ed
                   MOVE ac-valor-desconto TO ws-valor-ed
                   MOVE ac-dias-desconto TO ws-dias-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"categoria_id":' FUNCTION TRIM(ws-cat-id-ed)
                          ',"data":"' FUNCTION TRIM(ac-data) '"'
                          ',"descricao":"' FUNCTION TRIM(ac-descricao) '"'
                          ',"dias_desconto":' FUNCTION TRIM(ws-dias-ed)
                          ',"valor_desconto":' FUNCTION TRIM(ws-valor-ed)
                          ',"status":"' FUNCTION TRIM(ac-status) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE acao-file.

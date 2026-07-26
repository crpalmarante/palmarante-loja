       >>SOURCE FORMAT IS FREE
       *> emprestimo.cbl - CRUD de emprestimos a funcionarios
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Emprestimo.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT emp-file ASSIGN TO "dados/emprestimos.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/emprestimos.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD emp-file.
       01 emp-reg.
           05 emp-id                 PIC 9(4).
           05 emp-funcionario-id     PIC 9(3).
           05 emp-tipo               PIC X(30).
           05 emp-valor-total        PIC 9(7)V99.
           05 emp-num-parcelas       PIC 9(3).
           05 emp-valor-parcela      PIC 9(7)V99.
           05 emp-taxa-juros         PIC 9(3)V99.
           05 emp-data-solic         PIC X(10).
           05 emp-data-1-parcela     PIC X(10).
           05 emp-motivo             PIC X(200).
           05 emp-status             PIC X(1).
           05 emp-aprovado-por       PIC X(40).
           05 emp-data-aprovacao     PIC X(10).

       FD temp-file.
       01 temp-reg.
           05 tl-id                  PIC 9(4).
           05 tl-funcionario-id      PIC 9(3).
           05 tl-tipo                PIC X(30).
           05 tl-valor-total         PIC 9(7)V99.
           05 tl-num-parcelas        PIC 9(3).
           05 tl-valor-parcela       PIC 9(7)V99.
           05 tl-taxa-juros          PIC 9(3)V99.
           05 tl-data-solic          PIC X(10).
           05 tl-data-1-parcela      PIC X(10).
           05 tl-motivo              PIC X(200).
           05 tl-status              PIC X(1).
           05 tl-aprovado-por        PIC X(40).
           05 tl-data-aprovacao      PIC X(10).

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
       01 ws-tipo           PIC X(30).
       01 ws-valor-tot      PIC 9(7)V99.
       01 ws-valor-tot-ed   PIC Z(6)9.99.
       01 ws-valor-tot-in   PIC X(12).
       01 ws-num-parc       PIC 9(3).
       01 ws-num-parc-ed    PIC Z(3)9.
       01 ws-num-parc-in    PIC X(5).
       01 ws-valor-parc     PIC 9(7)V99.
       01 ws-valor-parc-ed  PIC Z(6)9.99.
       01 ws-valor-parc-in  PIC X(12).
       01 ws-taxa           PIC 9(3)V99.
       01 ws-taxa-ed        PIC Z(3)9.99.
       01 ws-taxa-in        PIC X(8).
       01 ws-data-solic     PIC X(10).
       01 ws-data-1-parc    PIC X(10).
       01 ws-motivo         PIC X(200).
       01 ws-status         PIC X(1).
       01 ws-aprov-por      PIC X(40).
       01 ws-data-aprov     PIC X(10).
       01 ws-json-linha     PIC X(700).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF
           EVALUATE ws-acao
               WHEN "incluir"        PERFORM incluir
               WHEN "alterar"        PERFORM alterar
               WHEN "excluir"        PERFORM excluir
                WHEN "aprovar"        PERFORM aprovar
                WHEN "rejeitar"       PERFORM rejeitar
                WHEN "transitar"      PERFORM transitar
                WHEN "listar"         PERFORM listar
               WHEN "listar-por-func" PERFORM listar-por-func
               WHEN "pendentes"      PERFORM pendentes
               WHEN "ativos"         PERFORM ativos
               WHEN "calcular-parcela" PERFORM calc-parcela
               WHEN OTHER            DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"
           ACCEPT ws-valor-tot-in FROM ENVIRONMENT "VALOR_TOTAL"
           COMPUTE ws-valor-tot = FUNCTION NUMVAL(ws-valor-tot-in)
           ACCEPT ws-num-parc-in FROM ENVIRONMENT "NUM_PARCELAS"
           COMPUTE ws-num-parc = FUNCTION NUMVAL(ws-num-parc-in)
           ACCEPT ws-valor-parc-in FROM ENVIRONMENT "VALOR_PARCELA"
           COMPUTE ws-valor-parc = FUNCTION NUMVAL(ws-valor-parc-in)
           ACCEPT ws-taxa-in FROM ENVIRONMENT "TAXA_JUROS"
           IF ws-taxa-in NOT = SPACES THEN
               COMPUTE ws-taxa = FUNCTION NUMVAL(ws-taxa-in)
           ELSE MOVE 0 TO ws-taxa END-IF
           ACCEPT ws-data-solic FROM ENVIRONMENT "DATA_SOLICITACAO"
           ACCEPT ws-data-1-parc FROM ENVIRONMENT "DATA_PRIMEIRA_PARCELA"
           ACCEPT ws-motivo FROM ENVIRONMENT "MOTIVO"
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"
           IF ws-status = SPACES THEN MOVE "P" TO ws-status END-IF
           MOVE 0 TO ws-prox-id
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT emp-file CLOSE emp-file
               OPEN INPUT emp-file END-IF
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-id > ws-prox-id THEN MOVE emp-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE emp-file
           ADD 1 TO ws-prox-id
           OPEN EXTEND emp-file
           MOVE ws-prox-id TO emp-id
           MOVE ws-func-id TO emp-funcionario-id
           MOVE ws-tipo TO emp-tipo
           MOVE ws-valor-tot TO emp-valor-total
           MOVE ws-num-parc TO emp-num-parcelas
           MOVE ws-valor-parc TO emp-valor-parcela
           MOVE ws-taxa TO emp-taxa-juros
           MOVE ws-data-solic TO emp-data-solic
            MOVE ws-data-1-parc TO emp-data-1-parcela
           MOVE ws-motivo TO emp-motivo
           MOVE ws-status TO emp-status
           MOVE SPACES TO emp-aprovado-por emp-data-aprovacao
           WRITE emp-reg
           CLOSE emp-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"
           ACCEPT ws-valor-tot-in FROM ENVIRONMENT "VALOR_TOTAL"
           ACCEPT ws-num-parc-in FROM ENVIRONMENT "NUM_PARCELAS"
           ACCEPT ws-valor-parc-in FROM ENVIRONMENT "VALOR_PARCELA"
           ACCEPT ws-taxa-in FROM ENVIRONMENT "TAXA_JUROS"
           ACCEPT ws-data-solic FROM ENVIRONMENT "DATA_SOLICITACAO"
           ACCEPT ws-data-1-parc FROM ENVIRONMENT "DATA_PRIMEIRA_PARCELA"
           ACCEPT ws-motivo FROM ENVIRONMENT "MOTIVO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-tipo NOT = SPACES THEN MOVE ws-tipo TO emp-tipo END-IF
                   IF ws-valor-tot-in NOT = SPACES THEN
                       COMPUTE ws-valor-tot = FUNCTION NUMVAL(ws-valor-tot-in)
                       MOVE ws-valor-tot TO emp-valor-total END-IF
                   IF ws-num-parc-in NOT = SPACES THEN
                       COMPUTE ws-num-parc = FUNCTION NUMVAL(ws-num-parc-in)
                       MOVE ws-num-parc TO emp-num-parcelas END-IF
                   IF ws-valor-parc-in NOT = SPACES THEN
                       COMPUTE ws-valor-parc = FUNCTION NUMVAL(ws-valor-parc-in)
                       MOVE ws-valor-parc TO emp-valor-parcela END-IF
                   IF ws-taxa-in NOT = SPACES THEN
                       COMPUTE ws-taxa = FUNCTION NUMVAL(ws-taxa-in)
                       MOVE ws-taxa TO emp-taxa-juros END-IF
                   IF ws-data-solic NOT = SPACES THEN
                       MOVE ws-data-solic TO emp-data-solic END-IF
                   IF ws-data-1-parc NOT = SPACES THEN
                       MOVE ws-data-1-parc TO emp-data-1-parcela END-IF
                   IF ws-motivo NOT = SPACES THEN
                       MOVE ws-motivo TO emp-motivo END-IF
               END-IF
               MOVE emp-id TO tl-id
               MOVE emp-funcionario-id TO tl-funcionario-id
               MOVE emp-tipo TO tl-tipo
               MOVE emp-valor-total TO tl-valor-total
               MOVE emp-num-parcelas TO tl-num-parcelas
               MOVE emp-valor-parcela TO tl-valor-parcela
               MOVE emp-taxa-juros TO tl-taxa-juros
               MOVE emp-data-solic TO tl-data-solic
               MOVE emp-data-1-parcela TO tl-data-1-parcela
               MOVE emp-motivo TO tl-motivo
               MOVE emp-status TO tl-status
               MOVE emp-aprovado-por TO tl-aprovado-por
               MOVE emp-data-aprovacao TO tl-data-aprovacao
               WRITE temp-reg
           END-PERFORM
           CLOSE emp-file CLOSE temp-file
           CALL "system" USING "mv dados/emprestimos.tmp dados/emprestimos.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-id NOT = ws-id THEN
                   MOVE emp-id TO tl-id
                   MOVE emp-funcionario-id TO tl-funcionario-id
                   MOVE emp-tipo TO tl-tipo
                   MOVE emp-valor-total TO tl-valor-total
                   MOVE emp-num-parcelas TO tl-num-parcelas
                   MOVE emp-valor-parcela TO tl-valor-parcela
                   MOVE emp-taxa-juros TO tl-taxa-juros
                   MOVE emp-data-solic TO tl-data-solic
                   MOVE emp-data-1-parcela TO tl-data-1-parcela
                   MOVE emp-motivo TO tl-motivo
                   MOVE emp-status TO tl-status
                   MOVE emp-aprovado-por TO tl-aprovado-por
                   MOVE emp-data-aprovacao TO tl-data-aprovacao
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou END-IF
           END-PERFORM
           CLOSE emp-file CLOSE temp-file
           CALL "system" USING "mv dados/emprestimos.tmp dados/emprestimos.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       aprovar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
           ACCEPT ws-data-aprov FROM ENVIRONMENT "DATA_APROVACAO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "A" TO emp-status
                   IF ws-aprov-por NOT = SPACES THEN
                       MOVE ws-aprov-por TO emp-aprovado-por END-IF
                   IF ws-data-aprov NOT = SPACES THEN
                       MOVE ws-data-aprov TO emp-data-aprovacao END-IF
               END-IF
               MOVE emp-id TO tl-id
               MOVE emp-funcionario-id TO tl-funcionario-id
               MOVE emp-tipo TO tl-tipo
               MOVE emp-valor-total TO tl-valor-total
               MOVE emp-num-parcelas TO tl-num-parcelas
               MOVE emp-valor-parcela TO tl-valor-parcela
               MOVE emp-taxa-juros TO tl-taxa-juros
               MOVE emp-data-solic TO tl-data-solic
               MOVE emp-data-1-parcela TO tl-data-1-parcela
               MOVE emp-motivo TO tl-motivo
               MOVE emp-status TO tl-status
               MOVE emp-aprovado-por TO tl-aprovado-por
               MOVE emp-data-aprovacao TO tl-data-aprovacao
               WRITE temp-reg
           END-PERFORM
           CLOSE emp-file CLOSE temp-file
           CALL "system" USING "mv dados/emprestimos.tmp dados/emprestimos.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       rejeitar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
           ACCEPT ws-data-aprov FROM ENVIRONMENT "DATA_APROVACAO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "R" TO emp-status
                   IF ws-aprov-por NOT = SPACES THEN
                       MOVE ws-aprov-por TO emp-aprovado-por END-IF
                   IF ws-data-aprov NOT = SPACES THEN
                       MOVE ws-data-aprov TO emp-data-aprovacao END-IF
               END-IF
               MOVE emp-id TO tl-id
               MOVE emp-funcionario-id TO tl-funcionario-id
               MOVE emp-tipo TO tl-tipo
               MOVE emp-valor-total TO tl-valor-total
               MOVE emp-num-parcelas TO tl-num-parcelas
               MOVE emp-valor-parcela TO tl-valor-parcela
               MOVE emp-taxa-juros TO tl-taxa-juros
               MOVE emp-data-solic TO tl-data-solic
               MOVE emp-data-1-parcela TO tl-data-1-parcela
               MOVE emp-motivo TO tl-motivo
               MOVE emp-status TO tl-status
               MOVE emp-aprovado-por TO tl-aprovado-por
               MOVE emp-data-aprovacao TO tl-data-aprovacao
               WRITE temp-reg
           END-PERFORM
           CLOSE emp-file CLOSE temp-file
           CALL "system" USING "mv dados/emprestimos.tmp dados/emprestimos.dat" END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

        transitar.
            ACCEPT ws-id-in FROM ENVIRONMENT "ID"
            COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
            ACCEPT ws-status FROM ENVIRONMENT "STATUS"
            ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
            ACCEPT ws-data-aprov FROM ENVIRONMENT "DATA_APROVACAO"
            MOVE "N" TO ws-encontrou
            OPEN INPUT emp-file
            IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
            OPEN OUTPUT temp-file
            PERFORM UNTIL 1 = 2
                READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
                IF emp-id = ws-id THEN
                    MOVE "S" TO ws-encontrou
                    MOVE ws-status TO emp-status
                    IF ws-aprov-por NOT = SPACES THEN
                        MOVE ws-aprov-por TO emp-aprovado-por END-IF
                    IF ws-data-aprov NOT = SPACES THEN
                        MOVE ws-data-aprov TO emp-data-aprovacao END-IF
                END-IF
                MOVE emp-id TO tl-id
                MOVE emp-funcionario-id TO tl-funcionario-id
                MOVE emp-tipo TO tl-tipo
                MOVE emp-valor-total TO tl-valor-total
                MOVE emp-num-parcelas TO tl-num-parcelas
                MOVE emp-valor-parcela TO tl-valor-parcela
                MOVE emp-taxa-juros TO tl-taxa-juros
                MOVE emp-data-solic TO tl-data-solic
                MOVE emp-data-1-parcela TO tl-data-1-parcela
                MOVE emp-motivo TO tl-motivo
                MOVE emp-status TO tl-status
                MOVE emp-aprovado-por TO tl-aprovado-por
                MOVE emp-data-aprovacao TO tl-data-aprovacao
                WRITE temp-reg
            END-PERFORM
            CLOSE emp-file CLOSE temp-file
            CALL "system" USING "mv dados/emprestimos.tmp dados/emprestimos.dat" END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

        calc-parcela.
           ACCEPT ws-valor-tot-in FROM ENVIRONMENT "VALOR_TOTAL"
           COMPUTE ws-valor-tot = FUNCTION NUMVAL(ws-valor-tot-in)
           ACCEPT ws-num-parc-in FROM ENVIRONMENT "NUM_PARCELAS"
           COMPUTE ws-num-parc = FUNCTION NUMVAL(ws-num-parc-in)
           ACCEPT ws-taxa-in FROM ENVIRONMENT "TAXA_JUROS"
           IF ws-taxa-in NOT = SPACES THEN
               COMPUTE ws-taxa = FUNCTION NUMVAL(ws-taxa-in)
           ELSE MOVE 0 TO ws-taxa END-IF
           IF ws-num-parc > 0 THEN
               IF ws-taxa > 0 THEN
                   COMPUTE ws-valor-parc ROUNDED =
                       ws-valor-tot * (ws-taxa / 100) /
                       (1 - (1 / (1 + ws-taxa / 100) ** ws-num-parc))
               ELSE
                   COMPUTE ws-valor-parc ROUNDED =
                       ws-valor-tot / ws-num-parc
               END-IF
           ELSE MOVE 0 TO ws-valor-parc END-IF
           MOVE ws-valor-parc TO ws-valor-parc-ed
           DISPLAY FUNCTION TRIM(ws-valor-parc-ed).

       listar.
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"emprestimos":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"emprestimos":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE emp-id TO ws-id-ed
               MOVE emp-funcionario-id TO ws-func-id-ed
               MOVE emp-valor-total TO ws-valor-tot-ed
               MOVE emp-num-parcelas TO ws-num-parc-ed
               MOVE emp-valor-parcela TO ws-valor-parc-ed
               MOVE emp-taxa-juros TO ws-taxa-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                      ',"tipo":"' FUNCTION TRIM(emp-tipo) '"'
                      ',"valor_total":' FUNCTION TRIM(ws-valor-tot-ed)
                      ',"num_parcelas":' FUNCTION TRIM(ws-num-parc-ed)
                      ',"valor_parcela":' FUNCTION TRIM(ws-valor-parc-ed)
                      ',"taxa_juros":' FUNCTION TRIM(ws-taxa-ed)
                      ',"data_solicitacao":"' FUNCTION TRIM(emp-data-solic) '"'
                      ',"data_primeira_parcela":"' FUNCTION TRIM(emp-data-1-parcela) '"'
                      ',"motivo":"' FUNCTION TRIM(emp-motivo) '"'
                      ',"status":"' FUNCTION TRIM(emp-status) '"'
                      ',"aprovado_por":"' FUNCTION TRIM(emp-aprovado-por) '"'
                      ',"data_aprovacao":"' FUNCTION TRIM(emp-data-aprovacao) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE emp-file.

       listar-por-func.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"emprestimos":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"emprestimos":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-funcionario-id = ws-func-id THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE emp-id TO ws-id-ed
                   MOVE emp-funcionario-id TO ws-func-id-ed
                   MOVE emp-valor-total TO ws-valor-tot-ed
                   MOVE emp-num-parcelas TO ws-num-parc-ed
                   MOVE emp-valor-parcela TO ws-valor-parc-ed
                   MOVE emp-taxa-juros TO ws-taxa-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"tipo":"' FUNCTION TRIM(emp-tipo) '"'
                          ',"valor_total":' FUNCTION TRIM(ws-valor-tot-ed)
                          ',"num_parcelas":' FUNCTION TRIM(ws-num-parc-ed)
                          ',"valor_parcela":' FUNCTION TRIM(ws-valor-parc-ed)
                          ',"taxa_juros":' FUNCTION TRIM(ws-taxa-ed)
                          ',"data_solicitacao":"' FUNCTION TRIM(emp-data-solic) '"'
                          ',"data_primeira_parcela":"' FUNCTION TRIM(emp-data-1-parcela) '"'
                          ',"motivo":"' FUNCTION TRIM(emp-motivo) '"'
                          ',"status":"' FUNCTION TRIM(emp-status) '"'
                          ',"aprovado_por":"' FUNCTION TRIM(emp-aprovado-por) '"'
                          ',"data_aprovacao":"' FUNCTION TRIM(emp-data-aprovacao) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE emp-file.

       pendentes.
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"emprestimos":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"emprestimos":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
                IF emp-status = "S" THEN
                    ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE emp-id TO ws-id-ed
                   MOVE emp-funcionario-id TO ws-func-id-ed
                   MOVE emp-valor-total TO ws-valor-tot-ed
                   MOVE emp-num-parcelas TO ws-num-parc-ed
                   MOVE emp-valor-parcela TO ws-valor-parc-ed
                   MOVE emp-taxa-juros TO ws-taxa-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"tipo":"' FUNCTION TRIM(emp-tipo) '"'
                          ',"valor_total":' FUNCTION TRIM(ws-valor-tot-ed)
                          ',"num_parcelas":' FUNCTION TRIM(ws-num-parc-ed)
                          ',"valor_parcela":' FUNCTION TRIM(ws-valor-parc-ed)
                          ',"taxa_juros":' FUNCTION TRIM(ws-taxa-ed)
                          ',"data_solicitacao":"' FUNCTION TRIM(emp-data-solic) '"'
                          ',"data_primeira_parcela":"' FUNCTION TRIM(emp-data-1-parcela) '"'
                          ',"motivo":"' FUNCTION TRIM(emp-motivo) '"'
                          ',"status":"' FUNCTION TRIM(emp-status) '"'
                          ',"aprovado_por":"' FUNCTION TRIM(emp-aprovado-por) '"'
                          ',"data_aprovacao":"' FUNCTION TRIM(emp-data-aprovacao) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE emp-file.

       ativos.
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"emprestimos":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"emprestimos":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ emp-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF emp-status = "A" THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE emp-id TO ws-id-ed
                   MOVE emp-funcionario-id TO ws-func-id-ed
                   MOVE emp-valor-total TO ws-valor-tot-ed
                   MOVE emp-num-parcelas TO ws-num-parc-ed
                   MOVE emp-valor-parcela TO ws-valor-parc-ed
                   MOVE emp-taxa-juros TO ws-taxa-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"tipo":"' FUNCTION TRIM(emp-tipo) '"'
                          ',"valor_total":' FUNCTION TRIM(ws-valor-tot-ed)
                          ',"num_parcelas":' FUNCTION TRIM(ws-num-parc-ed)
                          ',"valor_parcela":' FUNCTION TRIM(ws-valor-parc-ed)
                          ',"taxa_juros":' FUNCTION TRIM(ws-taxa-ed)
                          ',"data_solicitacao":"' FUNCTION TRIM(emp-data-solic) '"'
                          ',"data_primeira_parcela":"' FUNCTION TRIM(emp-data-1-parcela) '"'
                          ',"motivo":"' FUNCTION TRIM(emp-motivo) '"'
                          ',"status":"' FUNCTION TRIM(emp-status) '"'
                          ',"aprovado_por":"' FUNCTION TRIM(emp-aprovado-por) '"'
                          ',"data_aprovacao":"' FUNCTION TRIM(emp-data-aprovacao) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE emp-file.

       >>SOURCE FORMAT IS FREE
       *> licenca.cbl - CRUD de licencas/afastamentos
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Licenca.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT lic-file ASSIGN TO "dados/licencas.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/licencas.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD lic-file.
       01 lic-reg.
           05 lic-id              PIC 9(4).
           05 lic-funcionario-id  PIC 9(3).
           05 lic-tipo            PIC X(30).
           05 lic-data-inicio     PIC X(10).
           05 lic-data-fim        PIC X(10).
           05 lic-dias            PIC 9(3).
           05 lic-motivo          PIC X(200).
           05 lic-status          PIC X(1).
           05 lic-aprovado-por    PIC X(40).
           05 lic-data-aprovacao  PIC X(10).
           05 lic-observacoes     PIC X(200).

       FD temp-file.
       01 temp-reg.
           05 tl-id              PIC 9(4).
           05 tl-funcionario-id  PIC 9(3).
           05 tl-tipo            PIC X(30).
           05 tl-data-inicio     PIC X(10).
           05 tl-data-fim        PIC X(10).
           05 tl-dias            PIC 9(3).
           05 tl-motivo          PIC X(200).
           05 tl-status          PIC X(1).
           05 tl-aprovado-por    PIC X(40).
           05 tl-data-aprovacao  PIC X(10).
           05 tl-observacoes     PIC X(200).

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
       01 ws-dt-ini         PIC X(10).
       01 ws-dt-fim         PIC X(10).
       01 ws-dias           PIC 9(3).
       01 ws-dias-ed        PIC Z(3)9.
       01 ws-dias-in        PIC X(5).
       01 ws-motivo         PIC X(200).
       01 ws-status         PIC X(1).
       01 ws-aprov-por      PIC X(40).
       01 ws-dt-aprov       PIC X(10).
       01 ws-obs            PIC X(200).
       01 ws-json-linha     PIC X(600).

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
               WHEN OTHER            DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"
           ACCEPT ws-dt-ini FROM ENVIRONMENT "DATA_INICIO"
           ACCEPT ws-dt-fim FROM ENVIRONMENT "DATA_FIM"
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS"
           IF ws-dias-in NOT = SPACES THEN
               COMPUTE ws-dias = FUNCTION NUMVAL(ws-dias-in) END-IF
           ACCEPT ws-motivo FROM ENVIRONMENT "MOTIVO"
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"
           IF ws-status = SPACES THEN MOVE "P" TO ws-status END-IF
           ACCEPT ws-obs FROM ENVIRONMENT "OBSERVACOES"
           MOVE 0 TO ws-prox-id
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT lic-file CLOSE lic-file
               OPEN INPUT lic-file END-IF
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-id > ws-prox-id THEN MOVE lic-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE lic-file
           ADD 1 TO ws-prox-id
           OPEN EXTEND lic-file
           MOVE ws-prox-id TO lic-id
           MOVE ws-func-id TO lic-funcionario-id
           MOVE ws-tipo TO lic-tipo
           MOVE ws-dt-ini TO lic-data-inicio
           MOVE ws-dt-fim TO lic-data-fim
           MOVE ws-dias TO lic-dias
           MOVE ws-motivo TO lic-motivo
           MOVE ws-status TO lic-status
           MOVE SPACES TO lic-aprovado-por lic-data-aprovacao
           MOVE ws-obs TO lic-observacoes
           WRITE lic-reg
           CLOSE lic-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"
           ACCEPT ws-dt-ini FROM ENVIRONMENT "DATA_INICIO"
           ACCEPT ws-dt-fim FROM ENVIRONMENT "DATA_FIM"
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS"
           ACCEPT ws-motivo FROM ENVIRONMENT "MOTIVO"
           ACCEPT ws-obs FROM ENVIRONMENT "OBSERVACOES"
           MOVE "N" TO ws-encontrou
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-tipo NOT = SPACES THEN MOVE ws-tipo TO lic-tipo END-IF
                   IF ws-dt-ini NOT = SPACES THEN MOVE ws-dt-ini TO lic-data-inicio END-IF
                   IF ws-dt-fim NOT = SPACES THEN MOVE ws-dt-fim TO lic-data-fim END-IF
                   IF ws-dias-in NOT = SPACES THEN
                       COMPUTE ws-dias = FUNCTION NUMVAL(ws-dias-in)
                       MOVE ws-dias TO lic-dias END-IF
                   IF ws-motivo NOT = SPACES THEN MOVE ws-motivo TO lic-motivo END-IF
                   IF ws-obs NOT = SPACES THEN MOVE ws-obs TO lic-observacoes END-IF
               END-IF
               MOVE lic-id TO tl-id
               MOVE lic-funcionario-id TO tl-funcionario-id
               MOVE lic-tipo TO tl-tipo
               MOVE lic-data-inicio TO tl-data-inicio
               MOVE lic-data-fim TO tl-data-fim
               MOVE lic-dias TO tl-dias
               MOVE lic-motivo TO tl-motivo
               MOVE lic-status TO tl-status
               MOVE lic-aprovado-por TO tl-aprovado-por
               MOVE lic-data-aprovacao TO tl-data-aprovacao
               MOVE lic-observacoes TO tl-observacoes
               WRITE temp-reg
           END-PERFORM
           CLOSE lic-file CLOSE temp-file
           CALL "system" USING "mv dados/licencas.tmp dados/licencas.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-id NOT = ws-id THEN
                   MOVE lic-id TO tl-id MOVE lic-funcionario-id TO tl-funcionario-id
                   MOVE lic-tipo TO tl-tipo MOVE lic-data-inicio TO tl-data-inicio
                   MOVE lic-data-fim TO tl-data-fim MOVE lic-dias TO tl-dias
                   MOVE lic-motivo TO tl-motivo MOVE lic-status TO tl-status
                   MOVE lic-aprovado-por TO tl-aprovado-por
                   MOVE lic-data-aprovacao TO tl-data-aprovacao
                   MOVE lic-observacoes TO tl-observacoes
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou END-IF
           END-PERFORM
           CLOSE lic-file CLOSE temp-file
           CALL "system" USING "mv dados/licencas.tmp dados/licencas.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       aprovar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
           ACCEPT ws-dt-aprov FROM ENVIRONMENT "DATA_APROVACAO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "A" TO lic-status
                   IF ws-aprov-por NOT = SPACES THEN
                       MOVE ws-aprov-por TO lic-aprovado-por END-IF
                   IF ws-dt-aprov NOT = SPACES THEN
                       MOVE ws-dt-aprov TO lic-data-aprovacao END-IF
               END-IF
               MOVE lic-id TO tl-id MOVE lic-funcionario-id TO tl-funcionario-id
               MOVE lic-tipo TO tl-tipo MOVE lic-data-inicio TO tl-data-inicio
               MOVE lic-data-fim TO tl-data-fim MOVE lic-dias TO tl-dias
               MOVE lic-motivo TO tl-motivo MOVE lic-status TO tl-status
               MOVE lic-aprovado-por TO tl-aprovado-por
               MOVE lic-data-aprovacao TO tl-data-aprovacao
               MOVE lic-observacoes TO tl-observacoes
               WRITE temp-reg
           END-PERFORM
           CLOSE lic-file CLOSE temp-file
           CALL "system" USING "mv dados/licencas.tmp dados/licencas.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       rejeitar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
           ACCEPT ws-dt-aprov FROM ENVIRONMENT "DATA_APROVACAO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "R" TO lic-status
                   IF ws-aprov-por NOT = SPACES THEN
                       MOVE ws-aprov-por TO lic-aprovado-por END-IF
                   IF ws-dt-aprov NOT = SPACES THEN
                       MOVE ws-dt-aprov TO lic-data-aprovacao END-IF
               END-IF
               MOVE lic-id TO tl-id MOVE lic-funcionario-id TO tl-funcionario-id
               MOVE lic-tipo TO tl-tipo MOVE lic-data-inicio TO tl-data-inicio
               MOVE lic-data-fim TO tl-data-fim MOVE lic-dias TO tl-dias
               MOVE lic-motivo TO tl-motivo MOVE lic-status TO tl-status
               MOVE lic-aprovado-por TO tl-aprovado-por
               MOVE lic-data-aprovacao TO tl-data-aprovacao
               MOVE lic-observacoes TO tl-observacoes
               WRITE temp-reg
           END-PERFORM
           CLOSE lic-file CLOSE temp-file
           CALL "system" USING "mv dados/licencas.tmp dados/licencas.dat" END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

        transitar.
            ACCEPT ws-id-in FROM ENVIRONMENT "ID"
            COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
            ACCEPT ws-status FROM ENVIRONMENT "STATUS"
            ACCEPT ws-aprov-por FROM ENVIRONMENT "APROVADO_POR"
            ACCEPT ws-dt-aprov FROM ENVIRONMENT "DATA_APROVACAO"
            MOVE "N" TO ws-encontrou
            OPEN INPUT lic-file
            IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
            OPEN OUTPUT temp-file
            PERFORM UNTIL 1 = 2
                READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
                IF lic-id = ws-id THEN
                    MOVE "S" TO ws-encontrou
                    MOVE ws-status TO lic-status
                    IF ws-aprov-por NOT = SPACES THEN
                        MOVE ws-aprov-por TO lic-aprovado-por END-IF
                    IF ws-dt-aprov NOT = SPACES THEN
                        MOVE ws-dt-aprov TO lic-data-aprovacao END-IF
                END-IF
                MOVE lic-id TO tl-id MOVE lic-funcionario-id TO tl-funcionario-id
                MOVE lic-tipo TO tl-tipo MOVE lic-data-inicio TO tl-data-inicio
                MOVE lic-data-fim TO tl-data-fim MOVE lic-dias TO tl-dias
                MOVE lic-motivo TO tl-motivo MOVE lic-status TO tl-status
                MOVE lic-aprovado-por TO tl-aprovado-por
                MOVE lic-data-aprovacao TO tl-data-aprovacao
                MOVE lic-observacoes TO tl-observacoes
                WRITE temp-reg
            END-PERFORM
            CLOSE lic-file CLOSE temp-file
            CALL "system" USING "mv dados/licencas.tmp dados/licencas.dat" END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

        listar.
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"licencas":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"licencas":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE lic-id TO ws-id-ed
               MOVE lic-funcionario-id TO ws-func-id-ed
               MOVE lic-dias TO ws-dias-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                      ',"tipo":"' FUNCTION TRIM(lic-tipo) '"'
                      ',"data_inicio":"' FUNCTION TRIM(lic-data-inicio) '"'
                      ',"data_fim":"' FUNCTION TRIM(lic-data-fim) '"'
                      ',"dias":' FUNCTION TRIM(ws-dias-ed)
                      ',"motivo":"' FUNCTION TRIM(lic-motivo) '"'
                      ',"status":"' FUNCTION TRIM(lic-status) '"'
                      ',"aprovado_por":"' FUNCTION TRIM(lic-aprovado-por) '"'
                      ',"data_aprovacao":"' FUNCTION TRIM(lic-data-aprovacao) '"'
                      ',"observacoes":"' FUNCTION TRIM(lic-observacoes) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE lic-file.

       listar-por-func.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"licencas":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"licencas":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF lic-funcionario-id = ws-func-id THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE lic-id TO ws-id-ed
                   MOVE lic-funcionario-id TO ws-func-id-ed
                   MOVE lic-dias TO ws-dias-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"tipo":"' FUNCTION TRIM(lic-tipo) '"'
                          ',"data_inicio":"' FUNCTION TRIM(lic-data-inicio) '"'
                          ',"data_fim":"' FUNCTION TRIM(lic-data-fim) '"'
                          ',"dias":' FUNCTION TRIM(ws-dias-ed)
                          ',"motivo":"' FUNCTION TRIM(lic-motivo) '"'
                          ',"status":"' FUNCTION TRIM(lic-status) '"'
                          ',"aprovado_por":"' FUNCTION TRIM(lic-aprovado-por) '"'
                          ',"data_aprovacao":"' FUNCTION TRIM(lic-data-aprovacao) '"'
                          ',"observacoes":"' FUNCTION TRIM(lic-observacoes) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE lic-file.

       pendentes.
           OPEN INPUT lic-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"licencas":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"licencas":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ lic-file NEXT RECORD AT END EXIT PERFORM END-READ
                IF lic-status = "S" THEN
                    ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE lic-id TO ws-id-ed
                   MOVE lic-funcionario-id TO ws-func-id-ed
                   MOVE lic-dias TO ws-dias-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"tipo":"' FUNCTION TRIM(lic-tipo) '"'
                          ',"data_inicio":"' FUNCTION TRIM(lic-data-inicio) '"'
                          ',"data_fim":"' FUNCTION TRIM(lic-data-fim) '"'
                          ',"dias":' FUNCTION TRIM(ws-dias-ed)
                          ',"motivo":"' FUNCTION TRIM(lic-motivo) '"'
                          ',"status":"' FUNCTION TRIM(lic-status) '"'
                          ',"aprovado_por":"' FUNCTION TRIM(lic-aprovado-por) '"'
                          ',"data_aprovacao":"' FUNCTION TRIM(lic-data-aprovacao) '"'
                          ',"observacoes":"' FUNCTION TRIM(lic-observacoes) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE lic-file.

       >>SOURCE FORMAT IS FREE
       *> timesheet.cbl - CRUD folhas de horas
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Timesheet.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ts-file ASSIGN TO "dados/timesheets.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/timesheets.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD ts-file.
       01 ts-reg.
           05 ts-id                PIC 9(6).
           05 ts-funcionario-id    PIC 9(3).
           05 ts-data              PIC X(10).
           05 ts-projeto           PIC X(50).
           05 ts-tarefa            PIC X(50).
           05 ts-horas             PIC 9(4)V99.
           05 ts-descricao         PIC X(200).
           05 ts-status            PIC X(1).

       FD temp-file.
       01 temp-reg.
           05 tl-id                PIC 9(6).
           05 tl-funcionario-id    PIC 9(3).
           05 tl-data              PIC X(10).
           05 tl-projeto           PIC X(50).
           05 tl-tarefa            PIC X(50).
           05 tl-horas             PIC 9(4)V99.
           05 tl-descricao         PIC X(200).
           05 tl-status            PIC X(1).

       WORKING-STORAGE SECTION.
       01 ws-acao           PIC X(20).
       01 ws-file-status    PIC X(2).
       01 ws-encontrou      PIC X.
       01 ws-prox-id        PIC 9(6).
       01 ws-total          PIC 9(6).
       01 ws-total-ed       PIC Z(5)9.
       01 ws-id-ed          PIC Z(5)9.
       01 ws-id-in          PIC X(6).
       01 ws-id             PIC 9(6).
       01 ws-func-id        PIC 9(3).
       01 ws-func-id-ed     PIC Z(3)9.
       01 ws-func-id-in     PIC X(5).
       01 ws-data           PIC X(10).
       01 ws-projeto        PIC X(50).
       01 ws-tarefa         PIC X(50).
       01 ws-horas          PIC 9(4)V99.
       01 ws-horas-ed       PIC Z(4)9.99.
       01 ws-horas-in       PIC X(10).
       01 ws-descricao      PIC X(200).
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
               WHEN "listar-por-proj" PERFORM listar-por-projeto
               WHEN OTHER            DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-data FROM ENVIRONMENT "DATA"
           ACCEPT ws-projeto FROM ENVIRONMENT "PROJETO"
           ACCEPT ws-tarefa FROM ENVIRONMENT "TAREFA"
           ACCEPT ws-horas-in FROM ENVIRONMENT "HORAS"
           COMPUTE ws-horas = FUNCTION NUMVAL(ws-horas-in)
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"
           IF ws-status = SPACES THEN MOVE "P" TO ws-status END-IF
           MOVE 0 TO ws-prox-id
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT ts-file CLOSE ts-file
               OPEN INPUT ts-file END-IF
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF ts-id > ws-prox-id THEN MOVE ts-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE ts-file
           ADD 1 TO ws-prox-id
           OPEN EXTEND ts-file
           MOVE ws-prox-id TO ts-id
           MOVE ws-func-id TO ts-funcionario-id
           MOVE ws-data TO ts-data
           MOVE ws-projeto TO ts-projeto
           MOVE ws-tarefa TO ts-tarefa
           MOVE ws-horas TO ts-horas
           MOVE ws-descricao TO ts-descricao
           MOVE ws-status TO ts-status
           WRITE ts-reg
           CLOSE ts-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-projeto FROM ENVIRONMENT "PROJETO"
           ACCEPT ws-tarefa FROM ENVIRONMENT "TAREFA"
           ACCEPT ws-horas-in FROM ENVIRONMENT "HORAS"
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"
           ACCEPT ws-status FROM ENVIRONMENT "STATUS"
           MOVE "N" TO ws-encontrou
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF ts-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-projeto NOT = SPACES THEN MOVE ws-projeto TO ts-projeto END-IF
                   IF ws-tarefa NOT = SPACES THEN MOVE ws-tarefa TO ts-tarefa END-IF
                   IF ws-horas-in NOT = SPACES THEN
                       COMPUTE ws-horas = FUNCTION NUMVAL(ws-horas-in)
                       MOVE ws-horas TO ts-horas END-IF
                   IF ws-descricao NOT = SPACES THEN MOVE ws-descricao TO ts-descricao END-IF
                   IF ws-status NOT = SPACES THEN MOVE ws-status TO ts-status END-IF
               END-IF
               MOVE ts-id TO tl-id MOVE ts-funcionario-id TO tl-funcionario-id
               MOVE ts-data TO tl-data MOVE ts-projeto TO tl-projeto
               MOVE ts-tarefa TO tl-tarefa MOVE ts-horas TO tl-horas
               MOVE ts-descricao TO tl-descricao MOVE ts-status TO tl-status
               WRITE temp-reg
           END-PERFORM
           CLOSE ts-file CLOSE temp-file
           CALL "system" USING "mv dados/timesheets.tmp dados/timesheets.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF ts-id NOT = ws-id THEN
                   MOVE ts-id TO tl-id MOVE ts-funcionario-id TO tl-funcionario-id
                   MOVE ts-data TO tl-data MOVE ts-projeto TO tl-projeto
                   MOVE ts-tarefa TO tl-tarefa MOVE ts-horas TO tl-horas
                   MOVE ts-descricao TO tl-descricao MOVE ts-status TO tl-status
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou END-IF
           END-PERFORM
           CLOSE ts-file CLOSE temp-file
           CALL "system" USING "mv dados/timesheets.tmp dados/timesheets.dat" END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK" ELSE DISPLAY "ERRO".

       listar.
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"timesheets":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"timesheets":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE ts-id TO ws-id-ed
               MOVE ts-funcionario-id TO ws-func-id-ed
               MOVE ts-horas TO ws-horas-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                      ',"data":"' FUNCTION TRIM(ts-data) '"'
                      ',"projeto":"' FUNCTION TRIM(ts-projeto) '"'
                      ',"tarefa":"' FUNCTION TRIM(ts-tarefa) '"'
                      ',"horas":' FUNCTION TRIM(ws-horas-ed)
                      ',"descricao":"' FUNCTION TRIM(ts-descricao) '"'
                      ',"status":"' FUNCTION TRIM(ts-status) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE ts-file.

       listar-por-func.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"timesheets":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"timesheets":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF ts-funcionario-id = ws-func-id THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE ts-id TO ws-id-ed
                   MOVE ts-funcionario-id TO ws-func-id-ed
                   MOVE ts-horas TO ws-horas-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"data":"' FUNCTION TRIM(ts-data) '"'
                          ',"projeto":"' FUNCTION TRIM(ts-projeto) '"'
                          ',"tarefa":"' FUNCTION TRIM(ts-tarefa) '"'
                          ',"horas":' FUNCTION TRIM(ws-horas-ed)
                          ',"descricao":"' FUNCTION TRIM(ts-descricao) '"'
                          ',"status":"' FUNCTION TRIM(ts-status) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE ts-file.

       listar-por-projeto.
           ACCEPT ws-projeto FROM ENVIRONMENT "PROJETO"
           OPEN INPUT ts-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"timesheets":[],"total":0}' STOP RUN END-IF
           DISPLAY '{"timesheets":['
           MOVE "S" TO ws-encontrou MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ ts-file NEXT RECORD AT END EXIT PERFORM END-READ
               IF ts-projeto = ws-projeto THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE ts-id TO ws-id-ed
                   MOVE ts-funcionario-id TO ws-func-id-ed
                   MOVE ts-horas TO ws-horas-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"data":"' FUNCTION TRIM(ts-data) '"'
                          ',"projeto":"' FUNCTION TRIM(ts-projeto) '"'
                          ',"tarefa":"' FUNCTION TRIM(ts-tarefa) '"'
                          ',"horas":' FUNCTION TRIM(ws-horas-ed)
                          ',"descricao":"' FUNCTION TRIM(ts-descricao) '"'
                          ',"status":"' FUNCTION TRIM(ts-status) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE ts-file.

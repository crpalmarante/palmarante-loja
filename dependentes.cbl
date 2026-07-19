       >>SOURCE FORMAT IS FREE
       *> dependentes.cbl - CRUD de dependentes
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Dependentes.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT dp-file ASSIGN TO "dados/dependentes.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/dependentes.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD dp-file.
       01 dp-reg.
           05 dp-id              PIC 9(4).
           05 dp-funcionario-id  PIC 9(3).
           05 dp-nome            PIC X(40).
           05 dp-cpf             PIC X(14).
           05 dp-data-nasc       PIC X(10).
           05 dp-tipo            PIC X(15).

       FD temp-file.
       01 temp-reg.
           05 tl-id              PIC 9(4).
           05 tl-funcionario-id  PIC 9(3).
           05 tl-nome            PIC X(40).
           05 tl-cpf             PIC X(14).
           05 tl-data-nasc       PIC X(10).
           05 tl-tipo            PIC X(15).

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
       01 ws-nome           PIC X(40).
       01 ws-cpf            PIC X(14).
       01 ws-data-in        PIC X(10).
       01 ws-tipo           PIC X(15).
       01 ws-json-linha     PIC X(500).

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
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-cpf FROM ENVIRONMENT "CPF"
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_NASC"
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"

           MOVE 0 TO ws-prox-id
           OPEN INPUT dp-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT dp-file CLOSE dp-file
               OPEN INPUT dp-file END-IF
           PERFORM UNTIL 1 = 2
               READ dp-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF dp-id > ws-prox-id THEN MOVE dp-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE dp-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND dp-file
           MOVE ws-prox-id TO dp-id
           MOVE ws-func-id TO dp-funcionario-id
           MOVE ws-nome TO dp-nome
           MOVE ws-cpf TO dp-cpf
           MOVE ws-data-in TO dp-data-nasc
           MOVE ws-tipo TO dp-tipo
           WRITE dp-reg
           CLOSE dp-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           IF ws-func-id-in NOT = SPACES THEN
               COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in) END-IF
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-cpf FROM ENVIRONMENT "CPF"
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_NASC"
           ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"

           MOVE "N" TO ws-encontrou
           OPEN INPUT dp-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ dp-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF dp-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-func-id-in NOT = SPACES THEN
                       MOVE ws-func-id TO dp-funcionario-id END-IF
                   IF ws-nome NOT = SPACES THEN
                       MOVE ws-nome TO dp-nome END-IF
                   IF ws-cpf NOT = SPACES THEN
                       MOVE ws-cpf TO dp-cpf END-IF
                   IF ws-data-in NOT = SPACES THEN
                       MOVE ws-data-in TO dp-data-nasc END-IF
                   IF ws-tipo NOT = SPACES THEN
                       MOVE ws-tipo TO dp-tipo END-IF
               END-IF
               MOVE dp-id TO tl-id
               MOVE dp-funcionario-id TO tl-funcionario-id
               MOVE dp-nome TO tl-nome
               MOVE dp-cpf TO tl-cpf
               MOVE dp-data-nasc TO tl-data-nasc
               MOVE dp-tipo TO tl-tipo
               WRITE temp-reg
           END-PERFORM
           CLOSE dp-file CLOSE temp-file
           CALL "system" USING "mv dados/dependentes.tmp dados/dependentes.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT dp-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ dp-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF dp-id NOT = ws-id THEN
                   MOVE dp-id TO tl-id
                   MOVE dp-funcionario-id TO tl-funcionario-id
                   MOVE dp-nome TO tl-nome
                   MOVE dp-cpf TO tl-cpf
                   MOVE dp-data-nasc TO tl-data-nasc
                   MOVE dp-tipo TO tl-tipo
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE dp-file CLOSE temp-file
           CALL "system" USING "mv dados/dependentes.tmp dados/dependentes.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       listar.
           OPEN INPUT dp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"dependentes":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"dependentes":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ dp-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE dp-id TO ws-id-ed
               MOVE dp-funcionario-id TO ws-func-id-ed
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                      ',"nome":"' FUNCTION TRIM(dp-nome) '"'
                      ',"cpf":"' FUNCTION TRIM(dp-cpf) '"'
                      ',"data_nasc":"' FUNCTION TRIM(dp-data-nasc) '"'
                      ',"tipo":"' FUNCTION TRIM(dp-tipo) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE dp-file.

       listar-por-func.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)

           OPEN INPUT dp-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"dependentes":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"dependentes":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ dp-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF dp-funcionario-id = ws-func-id THEN
                   ADD 1 TO ws-total
                   IF ws-encontrou = "S" THEN
                       MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE dp-id TO ws-id-ed
                   MOVE dp-funcionario-id TO ws-func-id-ed
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                          ',"nome":"' FUNCTION TRIM(dp-nome) '"'
                          ',"cpf":"' FUNCTION TRIM(dp-cpf) '"'
                          ',"data_nasc":"' FUNCTION TRIM(dp-data-nasc) '"'
                          ',"tipo":"' FUNCTION TRIM(dp-tipo) '"}'
                      INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE dp-file.

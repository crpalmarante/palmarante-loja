        >>SOURCE FORMAT IS FREE
       *> ponto.cbl - Ponto Eletronico (clock in/out)
        IDENTIFICATION DIVISION.
        PROGRAM-ID. Ponto.

        ENVIRONMENT DIVISION.
        INPUT-OUTPUT SECTION.
        FILE-CONTROL.
            SELECT pon-file ASSIGN TO "dados/pontos.dat"
                ORGANIZATION IS LINE SEQUENTIAL
                FILE STATUS IS ws-file-status.
            SELECT temp-file ASSIGN TO "dados/pontos.tmp"
                ORGANIZATION IS LINE SEQUENTIAL.

        DATA DIVISION.
        FILE SECTION.
        FD pon-file.
        01 pon-reg.
            05 pon-id              PIC 9(6).
            05 pon-funcionario-id  PIC 9(3).
            05 pon-data            PIC X(10).
            05 pon-entrada         PIC X(5).
            05 pon-saida-almoco    PIC X(5).
            05 pon-volta-almoco    PIC X(5).
            05 pon-saida           PIC X(5).

        FD temp-file.
        01 temp-reg.
            05 tl-id               PIC 9(6).
            05 tl-funcionario-id   PIC 9(3).
            05 tl-data             PIC X(10).
            05 tl-entrada          PIC X(5).
            05 tl-saida-almoco     PIC X(5).
            05 tl-volta-almoco     PIC X(5).
            05 tl-saida            PIC X(5).

        WORKING-STORAGE SECTION.
        01 ws-acao           PIC X(20).
        01 ws-file-status    PIC X(2).
        01 ws-encontrou      PIC X.
        01 ws-prox-id        PIC 9(6).
        01 ws-total          PIC 9(6).
        01 ws-total-ed       PIC Z(5)9.
        01 ws-id-ed          PIC Z(5)9.
        01 ws-id-in          PIC X(7).
        01 ws-id             PIC 9(6).
        01 ws-func-id        PIC 9(3).
        01 ws-func-id-ed     PIC Z(2)9.
        01 ws-func-id-in     PIC X(5).
        01 ws-data           PIC X(10).
        01 ws-hora           PIC X(5).
        01 ws-tipo           PIC X(15).
        01 ws-entrada        PIC X(5).
        01 ws-saida-almoco   PIC X(5).
        01 ws-volta-almoco   PIC X(5).
        01 ws-saida          PIC X(5).
        01 ws-json-linha     PIC X(500).
        01 ws-mes            PIC X(2).
        01 ws-ano            PIC X(4).
        01 ws-mes-num        PIC 9(2).
        01 ws-ano-num        PIC 9(4).

        *> Time calculation for espelho
        01 ws-total-minutos  PIC 9(9).
        01 ws-total-horas    PIC 9(9).
        01 ws-horas-resto    PIC 9(9).
        01 ws-hora-entrada   PIC 9(2).
        01 ws-min-entrada    PIC 9(2).
        01 ws-hora-almoco    PIC 9(2).
        01 ws-min-almoco     PIC 9(2).
        01 ws-hora-volta     PIC 9(2).
        01 ws-min-volta      PIC 9(2).
        01 ws-hora-saida     PIC 9(2).
        01 ws-min-saida      PIC 9(2).
        01 ws-manha-min      PIC 9(9).
        01 ws-tarde-min      PIC 9(9).
        01 ws-dia-min        PIC 9(9).
        01 ws-horas-ed       PIC Z(5)9.
        01 ws-min-ed         PIC 9(2).
        01 ws-total-horas-str PIC X(10).
        01 ws-total-dias     PIC 9(6).
        01 ws-total-dias-ed  PIC Z(5)9.

        PROCEDURE DIVISION.

            ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
            IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

            EVALUATE ws-acao
                WHEN "bater"          PERFORM bater
                WHEN "listar"         PERFORM listar
                WHEN "listar-dia"     PERFORM listar-dia
                WHEN "espelho"        PERFORM espelho
                WHEN "alterar"        PERFORM alterar
                WHEN "excluir"        PERFORM excluir
                WHEN OTHER            DISPLAY "ERRO: acao invalida"
            END-EVALUATE
            STOP RUN.

        bater.
            ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
            COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
            ACCEPT ws-data FROM ENVIRONMENT "DATA"
            ACCEPT ws-hora FROM ENVIRONMENT "HORA"
            ACCEPT ws-tipo FROM ENVIRONMENT "TIPO"

            MOVE "N" TO ws-encontrou
            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                OPEN OUTPUT pon-file CLOSE pon-file
                OPEN INPUT pon-file
            END-IF

            MOVE 0 TO ws-prox-id
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF pon-id > ws-prox-id THEN
                    MOVE pon-id TO ws-prox-id
                END-IF
                IF pon-funcionario-id = ws-func-id
                   AND pon-data = ws-data THEN
                    MOVE "S" TO ws-encontrou
                    MOVE pon-id TO ws-id
                END-IF
            END-PERFORM
            CLOSE pon-file

            IF ws-encontrou = "S" THEN
                OPEN INPUT pon-file
                OPEN OUTPUT temp-file
                PERFORM UNTIL 1 = 2
                    READ pon-file NEXT RECORD
                        AT END EXIT PERFORM
                    END-READ
                    IF pon-id = ws-id THEN
                        EVALUATE ws-tipo
                            WHEN "entrada"
                                MOVE ws-hora TO pon-entrada
                            WHEN "almoco"
                                MOVE ws-hora TO pon-saida-almoco
                            WHEN "volta"
                                MOVE ws-hora TO pon-volta-almoco
                            WHEN "saida"
                                MOVE ws-hora TO pon-saida
                        END-EVALUATE
                    END-IF
                    MOVE pon-id TO tl-id
                    MOVE pon-funcionario-id TO tl-funcionario-id
                    MOVE pon-data TO tl-data
                    MOVE pon-entrada TO tl-entrada
                    MOVE pon-saida-almoco TO tl-saida-almoco
                    MOVE pon-volta-almoco TO tl-volta-almoco
                    MOVE pon-saida TO tl-saida
                    WRITE temp-reg
                END-PERFORM
                CLOSE pon-file CLOSE temp-file
                CALL "system" USING
                    "mv dados/pontos.tmp dados/pontos.dat"
                END-CALL
            ELSE
                ADD 1 TO ws-prox-id
                MOVE ws-prox-id TO ws-id
                OPEN EXTEND pon-file
                MOVE ws-prox-id TO pon-id
                MOVE ws-func-id TO pon-funcionario-id
                MOVE ws-data TO pon-data
                MOVE SPACES TO pon-entrada
                MOVE SPACES TO pon-saida-almoco
                MOVE SPACES TO pon-volta-almoco
                MOVE SPACES TO pon-saida
                EVALUATE ws-tipo
                    WHEN "entrada"
                        MOVE ws-hora TO pon-entrada
                    WHEN "almoco"
                        MOVE ws-hora TO pon-saida-almoco
                    WHEN "volta"
                        MOVE ws-hora TO pon-volta-almoco
                    WHEN "saida"
                        MOVE ws-hora TO pon-saida
                END-EVALUATE
                WRITE pon-reg
                CLOSE pon-file
            END-IF

            MOVE ws-id TO ws-id-ed
            DISPLAY FUNCTION TRIM(ws-id-ed).

        listar.
            ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
            ACCEPT ws-data FROM ENVIRONMENT "DATA"
            IF ws-func-id-in NOT = SPACES THEN
                COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
            ELSE
                MOVE 0 TO ws-func-id
            END-IF

            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                DISPLAY '{"pontos":[],"total":0}'
                STOP RUN
            END-IF

            DISPLAY '{"pontos":['
            MOVE "S" TO ws-encontrou
            MOVE 0 TO ws-total
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF (ws-func-id = 0
                    OR pon-funcionario-id = ws-func-id)
                   AND (ws-data = SPACES
                    OR pon-data = ws-data) THEN
                    ADD 1 TO ws-total
                    IF ws-encontrou = "S" THEN
                        MOVE "N" TO ws-encontrou
                    ELSE
                        DISPLAY ","
                    END-IF
                    MOVE pon-id TO ws-id-ed
                    MOVE pon-funcionario-id TO ws-func-id-ed
                    STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                           ',"funcionario_id":'
                           FUNCTION TRIM(ws-func-id-ed)
                           ',"data":"' FUNCTION TRIM(pon-data) '"'
                           ',"entrada":"'
                           FUNCTION TRIM(pon-entrada) '"'
                           ',"saida_almoco":"'
                           FUNCTION TRIM(pon-saida-almoco) '"'
                           ',"volta_almoco":"'
                           FUNCTION TRIM(pon-volta-almoco) '"'
                           ',"saida":"'
                           FUNCTION TRIM(pon-saida) '"}'
                        INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
                END-IF
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE pon-file.

        listar-dia.
            ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
            COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
            ACCEPT ws-data FROM ENVIRONMENT "DATA"

            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                DISPLAY '{}'
                STOP RUN
            END-IF

            MOVE "N" TO ws-encontrou
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF pon-funcionario-id = ws-func-id
                   AND pon-data = ws-data THEN
                    MOVE "S" TO ws-encontrou
                    MOVE pon-id TO ws-id-ed
                    MOVE pon-funcionario-id TO ws-func-id-ed
                    STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                           ',"funcionario_id":'
                           FUNCTION TRIM(ws-func-id-ed)
                           ',"data":"' FUNCTION TRIM(pon-data) '"'
                           ',"entrada":"'
                           FUNCTION TRIM(pon-entrada) '"'
                           ',"saida_almoco":"'
                           FUNCTION TRIM(pon-saida-almoco) '"'
                           ',"volta_almoco":"'
                           FUNCTION TRIM(pon-volta-almoco) '"'
                           ',"saida":"'
                           FUNCTION TRIM(pon-saida) '"}'
                        INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
                    EXIT PERFORM
                END-IF
            END-PERFORM
            CLOSE pon-file
            IF ws-encontrou = "N" THEN
                DISPLAY '{}'
            END-IF.

        espelho.
            ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
            COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
            ACCEPT ws-mes FROM ENVIRONMENT "MES"
            COMPUTE ws-mes-num = FUNCTION NUMVAL(ws-mes)
            ACCEPT ws-ano FROM ENVIRONMENT "ANO"
            COMPUTE ws-ano-num = FUNCTION NUMVAL(ws-ano)

            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                DISPLAY '{"pontos":[],"total_horas":"0:00",'
                       '"total_dias":0}'
                STOP RUN
            END-IF

            DISPLAY '{"pontos":['
            MOVE "S" TO ws-encontrou
            MOVE 0 TO ws-total
            MOVE 0 TO ws-total-minutos
            MOVE 0 TO ws-total-dias
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF pon-funcionario-id = ws-func-id
                   AND FUNCTION NUMVAL(pon-data(6:2)) = ws-mes-num
                   AND FUNCTION NUMVAL(pon-data(1:4)) = ws-ano-num THEN
                    ADD 1 TO ws-total
                    ADD 1 TO ws-total-dias
                    IF ws-encontrou = "S" THEN
                        MOVE "N" TO ws-encontrou
                    ELSE
                        DISPLAY ","
                    END-IF
                    MOVE pon-id TO ws-id-ed
                    MOVE pon-funcionario-id TO ws-func-id-ed
                    STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                           ',"funcionario_id":'
                           FUNCTION TRIM(ws-func-id-ed)
                           ',"data":"' FUNCTION TRIM(pon-data) '"'
                           ',"entrada":"'
                           FUNCTION TRIM(pon-entrada) '"'
                           ',"saida_almoco":"'
                           FUNCTION TRIM(pon-saida-almoco) '"'
                           ',"volta_almoco":"'
                           FUNCTION TRIM(pon-volta-almoco) '"'
                           ',"saida":"'
                           FUNCTION TRIM(pon-saida) '"}'
                        INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)

                    IF pon-entrada NOT = SPACES
                       AND pon-saida-almoco NOT = SPACES THEN
                        UNSTRING pon-entrada DELIMITED BY ":"
                            INTO ws-hora-entrada ws-min-entrada
                        UNSTRING pon-saida-almoco DELIMITED BY ":"
                            INTO ws-hora-almoco ws-min-almoco
                        COMPUTE ws-manha-min =
                            (ws-hora-almoco * 60 + ws-min-almoco)
                            - (ws-hora-entrada * 60 + ws-min-entrada)
                    ELSE
                        MOVE 0 TO ws-manha-min
                    END-IF
                    IF pon-volta-almoco NOT = SPACES
                       AND pon-saida NOT = SPACES THEN
                        UNSTRING pon-volta-almoco DELIMITED BY ":"
                            INTO ws-hora-volta ws-min-volta
                        UNSTRING pon-saida DELIMITED BY ":"
                            INTO ws-hora-saida ws-min-saida
                        COMPUTE ws-tarde-min =
                            (ws-hora-saida * 60 + ws-min-saida)
                            - (ws-hora-volta * 60 + ws-min-volta)
                    ELSE
                        MOVE 0 TO ws-tarde-min
                    END-IF
                    COMPUTE ws-dia-min = ws-manha-min + ws-tarde-min
                    IF ws-dia-min > 0 THEN
                        ADD ws-dia-min TO ws-total-minutos
                    END-IF
                END-IF
            END-PERFORM

            DIVIDE ws-total-minutos BY 60
                GIVING ws-total-horas REMAINDER ws-horas-resto
            MOVE ws-total-horas TO ws-horas-ed
            MOVE ws-horas-resto TO ws-min-ed
            STRING FUNCTION TRIM(ws-horas-ed) ":"
                   ws-min-ed
                INTO ws-total-horas-str

            MOVE ws-total TO ws-total-ed
            MOVE ws-total-dias TO ws-total-dias-ed

            DISPLAY '],"total_horas":"'
                    FUNCTION TRIM(ws-total-horas-str)
                    '","total_dias":'
                    FUNCTION TRIM(ws-total-dias-ed) '}'
            CLOSE pon-file.

        alterar.
            ACCEPT ws-id-in FROM ENVIRONMENT "ID"
            COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
            ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
            IF ws-func-id-in NOT = SPACES THEN
                COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
            END-IF
            ACCEPT ws-data FROM ENVIRONMENT "DATA"
            ACCEPT ws-entrada FROM ENVIRONMENT "ENTRADA"
            ACCEPT ws-saida-almoco FROM ENVIRONMENT "SAIDA_ALMOCO"
            ACCEPT ws-volta-almoco FROM ENVIRONMENT "VOLTA_ALMOCO"
            ACCEPT ws-saida FROM ENVIRONMENT "SAIDA"

            MOVE "N" TO ws-encontrou
            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                DISPLAY "ERRO" STOP RUN
            END-IF
            OPEN OUTPUT temp-file
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF pon-id = ws-id THEN
                    MOVE "S" TO ws-encontrou
                    IF ws-func-id-in NOT = SPACES THEN
                        MOVE ws-func-id TO pon-funcionario-id
                    END-IF
                    IF ws-data NOT = SPACES THEN
                        MOVE ws-data TO pon-data
                    END-IF
                    IF ws-entrada NOT = SPACES THEN
                        MOVE ws-entrada TO pon-entrada
                    END-IF
                    IF ws-saida-almoco NOT = SPACES THEN
                        MOVE ws-saida-almoco TO pon-saida-almoco
                    END-IF
                    IF ws-volta-almoco NOT = SPACES THEN
                        MOVE ws-volta-almoco TO pon-volta-almoco
                    END-IF
                    IF ws-saida NOT = SPACES THEN
                        MOVE ws-saida TO pon-saida
                    END-IF
                END-IF
                MOVE pon-id TO tl-id
                MOVE pon-funcionario-id TO tl-funcionario-id
                MOVE pon-data TO tl-data
                MOVE pon-entrada TO tl-entrada
                MOVE pon-saida-almoco TO tl-saida-almoco
                MOVE pon-volta-almoco TO tl-volta-almoco
                MOVE pon-saida TO tl-saida
                WRITE temp-reg
            END-PERFORM
            CLOSE pon-file CLOSE temp-file
            CALL "system" USING
                "mv dados/pontos.tmp dados/pontos.dat"
            END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK"
            ELSE DISPLAY "ERRO".

        excluir.
            ACCEPT ws-id-in FROM ENVIRONMENT "ID"
            COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

            MOVE "N" TO ws-encontrou
            OPEN INPUT pon-file
            IF ws-file-status = "35" THEN
                DISPLAY "ERRO" STOP RUN
            END-IF
            OPEN OUTPUT temp-file
            PERFORM UNTIL 1 = 2
                READ pon-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                IF pon-id NOT = ws-id THEN
                    MOVE pon-id TO tl-id
                    MOVE pon-funcionario-id TO tl-funcionario-id
                    MOVE pon-data TO tl-data
                    MOVE pon-entrada TO tl-entrada
                    MOVE pon-saida-almoco TO tl-saida-almoco
                    MOVE pon-volta-almoco TO tl-volta-almoco
                    MOVE pon-saida TO tl-saida
                    WRITE temp-reg
                ELSE
                    MOVE "S" TO ws-encontrou
                END-IF
            END-PERFORM
            CLOSE pon-file CLOSE temp-file
            CALL "system" USING
                "mv dados/pontos.tmp dados/pontos.dat"
            END-CALL
            IF ws-encontrou = "S" THEN DISPLAY "OK"
            ELSE DISPLAY "ERRO".

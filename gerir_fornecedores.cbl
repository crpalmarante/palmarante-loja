       >>SOURCE FORMAT IS FREE
       *> gerir_fornecedores.cbl - CRUD fornecedores
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirFornecedores.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT forn-file ASSIGN TO "dados/fornecedores.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/fornecedores.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD forn-file.
       01 forn-reg.
           05 fn-id             PIC 9(5).
           05 fn-cnpj           PIC X(18).
           05 fn-nome           PIC X(60).
           05 fn-endereco       PIC X(60).
           05 fn-telefone       PIC X(15).
           05 fn-email          PIC X(40).
           05 fn-ie             PIC X(20).
           05 fn-inscricao-mun  PIC X(20).

       FD temp-file.
       01 temp-reg.
           05 tn-id             PIC 9(5).
           05 tn-cnpj           PIC X(18).
           05 tn-nome           PIC X(60).
           05 tn-endereco       PIC X(60).
           05 tn-telefone       PIC X(15).
           05 tn-email          PIC X(40).
           05 tn-ie             PIC X(20).
           05 tn-inscricao-mun  PIC X(20).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-existe          PIC X(1).
       01 ws-json-linha      PIC X(500).
       01 ws-id-ed           PIC ZZZZ9.
       01 ws-total-ed        PIC ZZZZ9.
       01 ws-id              PIC 9(5).
       01 ws-id-in           PIC X(10).
       01 ws-nome            PIC X(60).
       01 ws-cnpj            PIC X(18).
       01 ws-endereco        PIC X(60).
       01 ws-telefone        PIC X(15).
       01 ws-email           PIC X(40).
       01 ws-ie              PIC X(20).
       01 ws-inscricao-mun   PIC X(20).
        01 ws-encontrou       PIC X(1).
        01 ws-prox-id         PIC 9(5).
        01 ws-cnpj-trim       PIC X(18).
        01 ws-cnpj-arq        PIC X(18).
        01 ws-i               PIC 9(2).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "alterar"  PERFORM alterar
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN "buscar-cnpj" PERFORM buscar-cnpj
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-cnpj FROM ENVIRONMENT "CNPJ"
           ACCEPT ws-endereco FROM ENVIRONMENT "ENDERECO"
           ACCEPT ws-telefone FROM ENVIRONMENT "TELEFONE"
           ACCEPT ws-email FROM ENVIRONMENT "EMAIL"
           ACCEPT ws-ie FROM ENVIRONMENT "IE"
           ACCEPT ws-inscricao-mun FROM ENVIRONMENT "INSCRICAO_MUN"
           IF ws-nome = SPACES THEN
               DISPLAY "ERRO: nome obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT forn-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT forn-file CLOSE forn-file
               OPEN INPUT forn-file END-IF
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fn-id > ws-prox-id THEN MOVE fn-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE forn-file

           ADD 1 TO ws-prox-id
           OPEN EXTEND forn-file
           MOVE ws-prox-id TO fn-id
           MOVE ws-nome TO fn-nome
           MOVE ws-cnpj TO fn-cnpj
           MOVE ws-endereco TO fn-endereco
           MOVE ws-telefone TO fn-telefone
           MOVE ws-email TO fn-email
           MOVE ws-ie TO fn-ie
           MOVE ws-inscricao-mun TO fn-inscricao-mun
           WRITE forn-reg
           CLOSE forn-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-cnpj FROM ENVIRONMENT "CNPJ"
           ACCEPT ws-endereco FROM ENVIRONMENT "ENDERECO"
           ACCEPT ws-telefone FROM ENVIRONMENT "TELEFONE"
           ACCEPT ws-email FROM ENVIRONMENT "EMAIL"
           ACCEPT ws-ie FROM ENVIRONMENT "IE"
           ACCEPT ws-inscricao-mun FROM ENVIRONMENT "INSCRICAO_MUN"

           MOVE "N" TO ws-encontrou
           OPEN INPUT forn-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: fornecedor nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fn-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN MOVE ws-nome TO fn-nome END-IF
                   IF ws-cnpj NOT = SPACES THEN MOVE ws-cnpj TO fn-cnpj END-IF
                   IF ws-endereco NOT = SPACES THEN MOVE ws-endereco TO fn-endereco END-IF
                   IF ws-telefone NOT = SPACES THEN MOVE ws-telefone TO fn-telefone END-IF
                   IF ws-email NOT = SPACES THEN MOVE ws-email TO fn-email END-IF
                   IF ws-ie NOT = SPACES THEN MOVE ws-ie TO fn-ie END-IF
                   IF ws-inscricao-mun NOT = SPACES THEN MOVE ws-inscricao-mun TO fn-inscricao-mun END-IF
               END-IF
               MOVE fn-id TO tn-id
               MOVE fn-nome TO tn-nome
               MOVE fn-cnpj TO tn-cnpj
               MOVE fn-endereco TO tn-endereco
               MOVE fn-telefone TO tn-telefone
               MOVE fn-email TO tn-email
               MOVE fn-ie TO tn-ie
               MOVE fn-inscricao-mun TO tn-inscricao-mun
               WRITE temp-reg
           END-PERFORM
           CLOSE forn-file CLOSE temp-file
           CALL "system" USING "mv dados/fornecedores.tmp dados/fornecedores.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: fornecedor nao encontrado".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT forn-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: fornecedor nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fn-id NOT = ws-id THEN
                   MOVE fn-id TO tn-id
                   MOVE fn-nome TO tn-nome
                   MOVE fn-cnpj TO tn-cnpj
                   MOVE fn-endereco TO tn-endereco
                   MOVE fn-telefone TO tn-telefone
                   MOVE fn-email TO tn-email
                   MOVE fn-ie TO tn-ie
                   MOVE fn-inscricao-mun TO tn-inscricao-mun
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE forn-file CLOSE temp-file
           CALL "system" USING "mv dados/fornecedores.tmp dados/fornecedores.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: fornecedor nao encontrado".

       listar.
           OPEN INPUT forn-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"fornecedores":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"fornecedores":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-prox-id
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-prox-id
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE
                   DISPLAY ","
               END-IF
               MOVE fn-id TO ws-id-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"cnpj":"' FUNCTION TRIM(fn-cnpj) '"'
                      ',"nome":"' FUNCTION TRIM(fn-nome) '"'
                      ',"endereco":"' FUNCTION TRIM(fn-endereco) '"'
                      ',"telefone":"' FUNCTION TRIM(fn-telefone) '"'
                      ',"email":"' FUNCTION TRIM(fn-email) '"'
                      ',"ie":"' FUNCTION TRIM(fn-ie) '"'
                      ',"inscricao_mun":"' FUNCTION TRIM(fn-inscricao-mun) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-prox-id TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE forn-file.

        buscar-cnpj.
            ACCEPT ws-cnpj FROM ENVIRONMENT "CNPJ"
            MOVE SPACES TO ws-cnpj-trim
            MOVE 1 TO ws-i
            PERFORM VARYING ws-i FROM 1 BY 1 UNTIL ws-i > 18
                IF ws-cnpj(ws-i:1) NOT = SPACE
                    STRING ws-cnpj-trim DELIMITED BY SPACES
                           ws-cnpj(ws-i:1) DELIMITED BY SIZE
                           INTO ws-cnpj-trim
                END-IF
            END-PERFORM
            OPEN INPUT forn-file
            IF ws-file-status = "35" THEN
                DISPLAY '{"status":"erro","mensagem":"nao encontrado"}'
                STOP RUN END-IF
            MOVE "N" TO ws-encontrou
            PERFORM UNTIL 1 = 2
                READ forn-file NEXT RECORD
                    AT END EXIT PERFORM
                END-READ
                MOVE SPACES TO ws-cnpj-arq
                MOVE 1 TO ws-i
                PERFORM VARYING ws-i FROM 1 BY 1 UNTIL ws-i > 18
                    IF fn-cnpj(ws-i:1) NOT = SPACE
                        STRING ws-cnpj-arq DELIMITED BY SPACES
                               fn-cnpj(ws-i:1) DELIMITED BY SIZE
                               INTO ws-cnpj-arq
                    END-IF
                END-PERFORM
                IF ws-cnpj-trim = ws-cnpj-arq
                    MOVE SPACES TO ws-json-linha
                    MOVE fn-id TO ws-id-ed
                    STRING '{"status":"ok","id":' FUNCTION TRIM(ws-id-ed)
                           ',"cnpj":"' FUNCTION TRIM(fn-cnpj) '"'
                           ',"nome":"' FUNCTION TRIM(fn-nome) '"'
                           ',"endereco":"' FUNCTION TRIM(fn-endereco) '"'
                           ',"telefone":"' FUNCTION TRIM(fn-telefone) '"'
                           ',"email":"' FUNCTION TRIM(fn-email) '"'
                           ',"ie":"' FUNCTION TRIM(fn-ie) '"'
                           ',"inscricao_mun":"' FUNCTION TRIM(fn-inscricao-mun) '"}'
                        INTO ws-json-linha
                    DISPLAY FUNCTION TRIM(ws-json-linha)
                    MOVE "S" TO ws-encontrou
                END-IF
            END-PERFORM
            CLOSE forn-file
            IF ws-encontrou = "N" THEN
                DISPLAY '{"status":"erro","mensagem":"nao encontrado"}' END-IF.

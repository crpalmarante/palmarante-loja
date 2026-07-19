       >>SOURCE FORMAT IS FREE
       *> categoria_disciplinar.cbl - CRUD de categorias disciplinares
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CategoriaDisciplinar.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT cat-file ASSIGN TO "dados/categorias_disciplinares.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/categorias_disciplinares.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD cat-file.
       01 cat-reg.
           05 cat-id           PIC 9(4).
           05 cat-nome         PIC X(40).
           05 cat-descricao    PIC X(100).

       FD temp-file.
       01 temp-reg.
           05 tl-id            PIC 9(4).
           05 tl-nome          PIC X(40).
           05 tl-descricao     PIC X(100).

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
       01 ws-nome           PIC X(40).
       01 ws-descricao      PIC X(100).
       01 ws-json-linha     PIC X(500).

       PROCEDURE DIVISION.

           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"        PERFORM incluir
               WHEN "alterar"        PERFORM alterar
               WHEN "excluir"        PERFORM excluir
               WHEN "listar"         PERFORM listar
               WHEN OTHER            DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"

           MOVE 0 TO ws-prox-id
           OPEN INPUT cat-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT cat-file CLOSE cat-file
               OPEN INPUT cat-file END-IF
           PERFORM UNTIL 1 = 2
               READ cat-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF cat-id > ws-prox-id THEN MOVE cat-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE cat-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND cat-file
           MOVE ws-prox-id TO cat-id
           MOVE ws-nome TO cat-nome
           MOVE ws-descricao TO cat-descricao
           WRITE cat-reg
           CLOSE cat-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-descricao FROM ENVIRONMENT "DESCRICAO"

           MOVE "N" TO ws-encontrou
           OPEN INPUT cat-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ cat-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF cat-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN
                       MOVE ws-nome TO cat-nome END-IF
                   IF ws-descricao NOT = SPACES THEN
                       MOVE ws-descricao TO cat-descricao END-IF
               END-IF
               MOVE cat-id TO tl-id
               MOVE cat-nome TO tl-nome
               MOVE cat-descricao TO tl-descricao
               WRITE temp-reg
           END-PERFORM
           CLOSE cat-file CLOSE temp-file
           CALL "system" USING "mv dados/categorias_disciplinares.tmp dados/categorias_disciplinares.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT cat-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ cat-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF cat-id NOT = ws-id THEN
                   MOVE cat-id TO tl-id
                   MOVE cat-nome TO tl-nome
                   MOVE cat-descricao TO tl-descricao
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE cat-file CLOSE temp-file
           CALL "system" USING "mv dados/categorias_disciplinares.tmp dados/categorias_disciplinares.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       listar.
           OPEN INPUT cat-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"categorias":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"categorias":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ cat-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE cat-id TO ws-id-ed
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"nome":"' FUNCTION TRIM(cat-nome) '"'
                      ',"descricao":"' FUNCTION TRIM(cat-descricao) '"}'
                  INTO ws-json-linha
                DISPLAY FUNCTION TRIM(ws-json-linha)
            END-PERFORM
            MOVE ws-total TO ws-total-ed
            DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
            CLOSE cat-file.

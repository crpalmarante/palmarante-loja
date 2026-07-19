       >>SOURCE FORMAT IS FREE
       *> gerir_usuarios.cbl - CRUD de usuarios administradores
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirUsuarios.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT us-file ASSIGN TO "dados/usuarios.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/usuarios.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD us-file.
       01 us-reg.
           05 us-id          PIC 9(3).
           05 us-nome        PIC X(40).
           05 us-usuario     PIC X(20).
           05 us-senha       PIC X(20).
           05 us-nivel       PIC X.
           05 us-ativo       PIC X.

       FD temp-file.
       01 temp-reg.
           05 tl-id          PIC 9(3).
           05 tl-nome        PIC X(40).
           05 tl-usuario     PIC X(20).
           05 tl-senha       PIC X(20).
           05 tl-nivel       PIC X.
           05 tl-ativo       PIC X.

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-encontrou       PIC X(1).
       01 ws-json-linha      PIC X(300).
       01 ws-id-ed           PIC ZZZ9.
       01 ws-total-ed        PIC ZZZ9.
       01 ws-id              PIC 9(3).
       01 ws-id-in           PIC X(5).
       01 ws-nome            PIC X(40).
       01 ws-usuario         PIC X(20).
       01 ws-senha           PIC X(20).
       01 ws-nivel           PIC X.
       01 ws-prox-id         PIC 9(3).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "alterar"  PERFORM alterar
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN "login"    PERFORM login
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-usuario FROM ENVIRONMENT "USUARIO"
           ACCEPT ws-senha FROM ENVIRONMENT "SENHA"
           ACCEPT ws-nivel FROM ENVIRONMENT "NIVEL"
           IF ws-nome = SPACES THEN
               DISPLAY "ERRO: nome obrigatorio" STOP RUN END-IF
           IF ws-usuario = SPACES THEN
               DISPLAY "ERRO: usuario obrigatorio" STOP RUN END-IF
           IF ws-senha = SPACES THEN
               DISPLAY "ERRO: senha obrigatoria" STOP RUN END-IF
           IF ws-nivel = SPACES THEN MOVE "A" TO ws-nivel END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT us-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT us-file CLOSE us-file
               OPEN INPUT us-file END-IF
           PERFORM UNTIL 1 = 2
               READ us-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF us-id > ws-prox-id THEN MOVE us-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE us-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND us-file
           MOVE ws-prox-id TO us-id
           MOVE ws-nome TO us-nome
           MOVE ws-usuario TO us-usuario
           MOVE ws-senha TO us-senha
           MOVE ws-nivel TO us-nivel
           MOVE "S" TO us-ativo
           WRITE us-reg
           CLOSE us-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-usuario FROM ENVIRONMENT "USUARIO"
           ACCEPT ws-senha FROM ENVIRONMENT "SENHA"
           ACCEPT ws-nivel FROM ENVIRONMENT "NIVEL"

           MOVE "N" TO ws-encontrou
           OPEN INPUT us-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: usuario nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ us-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF us-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN MOVE ws-nome TO us-nome END-IF
                   IF ws-usuario NOT = SPACES THEN
                       MOVE ws-usuario TO us-usuario END-IF
                   IF ws-senha NOT = SPACES THEN
                       MOVE ws-senha TO us-senha END-IF
                   IF ws-nivel NOT = SPACES THEN
                       MOVE ws-nivel TO us-nivel END-IF
               END-IF
               MOVE us-id TO tl-id
               MOVE us-nome TO tl-nome
               MOVE us-usuario TO tl-usuario
               MOVE us-senha TO tl-senha
               MOVE us-nivel TO tl-nivel
               MOVE us-ativo TO tl-ativo
               WRITE temp-reg
           END-PERFORM
           CLOSE us-file CLOSE temp-file
           CALL "system" USING "mv dados/usuarios.tmp dados/usuarios.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: usuario nao encontrado".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT us-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: usuario nao encontrado" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ us-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF us-id NOT = ws-id THEN
                   MOVE us-id TO tl-id
                   MOVE us-nome TO tl-nome
                   MOVE us-usuario TO tl-usuario
                   MOVE us-senha TO tl-senha
                   MOVE us-nivel TO tl-nivel
                   MOVE us-ativo TO tl-ativo
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE us-file CLOSE temp-file
           CALL "system" USING "mv dados/usuarios.tmp dados/usuarios.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: usuario nao encontrado".

       login.
           ACCEPT ws-usuario FROM ENVIRONMENT "USUARIO"
           ACCEPT ws-senha FROM ENVIRONMENT "SENHA"
           IF ws-usuario = SPACES OR ws-senha = SPACES THEN
               DISPLAY '{"status":"erro","mensagem":"usuario e senha obrigatorios"}'
               STOP RUN END-IF

           OPEN INPUT us-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"status":"erro","mensagem":"nenhum usuario cadastrado"}'
               STOP RUN END-IF
           MOVE "N" TO ws-encontrou
           PERFORM UNTIL 1 = 2
               READ us-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF us-usuario = ws-usuario AND us-senha = ws-senha
                   AND us-ativo = "S" THEN
                   MOVE "S" TO ws-encontrou
                   MOVE us-id TO ws-id-ed
                   DISPLAY '{"status":"ok","tipo":"usuario"'
                       ',"id":' FUNCTION TRIM(ws-id-ed)
                       ',"nome":"' FUNCTION TRIM(us-nome) '"'
                       ',"usuario":"' FUNCTION TRIM(us-usuario) '"'
                       ',"nivel":"' FUNCTION TRIM(us-nivel) '"}'
                   EXIT PERFORM
               END-IF
           END-PERFORM
           CLOSE us-file
           IF ws-encontrou = "N" THEN
               DISPLAY '{"status":"erro","mensagem":"usuario ou senha incorretos"}'
           END-IF.

       listar.
           OPEN INPUT us-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"usuarios":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"usuarios":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-prox-id
           PERFORM UNTIL 1 = 2
               READ us-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-prox-id
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE us-id TO ws-id-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"nome":"' FUNCTION TRIM(us-nome) '"'
                      ',"usuario":"' FUNCTION TRIM(us-usuario) '"'
                      ',"nivel":"' FUNCTION TRIM(us-nivel) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-prox-id TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE us-file.

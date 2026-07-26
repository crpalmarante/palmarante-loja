       >>SOURCE FORMAT IS FREE
       *> gerir_filiais.cbl - CRUD de filiais
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirFiliais.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT fil-file ASSIGN TO "dados/filiais.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/filiais.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD fil-file.
       01 fil-reg.
           05 fl-id           PIC 9(3).
           05 fl-nome         PIC X(50).
           05 fl-endereco     PIC X(50).
           05 fl-responsavel  PIC X(50).

       FD temp-file.
       01 temp-reg.
           05 tl-id           PIC 9(3).
           05 tl-nome         PIC X(50).
           05 tl-endereco     PIC X(50).
           05 tl-responsavel  PIC X(50).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-existe          PIC X(1).
       01 ws-json-linha      PIC X(300).
       01 ws-id-ed           PIC ZZZ9.
       01 ws-total-ed        PIC ZZZ9.
       01 ws-id              PIC 9(3).
       01 ws-id-in           PIC X(5).
       01 ws-nome            PIC X(50).
       01 ws-endereco        PIC X(50).
       01 ws-responsavel     PIC X(50).
       01 ws-encontrou       PIC X(1).
       01 ws-prox-id         PIC 9(3).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "alterar"  PERFORM alterar
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-endereco FROM ENVIRONMENT "ENDERECO"
           ACCEPT ws-responsavel FROM ENVIRONMENT "RESPONSAVEL"
           IF ws-nome = SPACES THEN
               DISPLAY "ERRO: nome obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT fil-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT fil-file CLOSE fil-file
               OPEN INPUT fil-file END-IF
           PERFORM UNTIL 1 = 2
               READ fil-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fl-id > ws-prox-id THEN MOVE fl-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE fil-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND fil-file
           MOVE ws-prox-id TO fl-id
           MOVE ws-nome TO fl-nome
           MOVE ws-endereco TO fl-endereco
           MOVE ws-responsavel TO fl-responsavel
           WRITE fil-reg
           CLOSE fil-file
           DISPLAY ws-prox-id.

       alterar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-endereco FROM ENVIRONMENT "ENDERECO"
           ACCEPT ws-responsavel FROM ENVIRONMENT "RESPONSAVEL"

           MOVE "N" TO ws-encontrou
           OPEN INPUT fil-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: filial nao encontrada" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ fil-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fl-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   IF ws-nome NOT = SPACES THEN MOVE ws-nome TO fl-nome END-IF
                   IF ws-endereco NOT = SPACES THEN
                       MOVE ws-endereco TO fl-endereco END-IF
                   IF ws-responsavel NOT = SPACES THEN
                       MOVE ws-responsavel TO fl-responsavel END-IF
               END-IF
               MOVE fl-id TO tl-id
               MOVE fl-nome TO tl-nome
               MOVE fl-endereco TO tl-endereco
               MOVE fl-responsavel TO tl-responsavel
               WRITE temp-reg
           END-PERFORM
           CLOSE fil-file CLOSE temp-file
           CALL "system" USING "mv dados/filiais.tmp dados/filiais.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: filial nao encontrada".

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT fil-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: filial nao encontrada" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ fil-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fl-id NOT = ws-id THEN
                   MOVE fl-id TO tl-id
                   MOVE fl-nome TO tl-nome
                   MOVE fl-endereco TO tl-endereco
                   MOVE fl-responsavel TO tl-responsavel
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE fil-file CLOSE temp-file
           CALL "system" USING "mv dados/filiais.tmp dados/filiais.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: filial nao encontrada".

       listar.
           OPEN INPUT fil-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"filiais":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"filiais":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-prox-id
           PERFORM UNTIL 1 = 2
               READ fil-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-prox-id
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE
                   DISPLAY ","
               END-IF
               MOVE fl-id TO ws-id-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"nome":"' FUNCTION TRIM(fl-nome) '"'
                      ',"endereco":"' FUNCTION TRIM(fl-endereco) '"'
                      ',"responsavel":"' FUNCTION TRIM(fl-responsavel) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-prox-id TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE fil-file.

       >>SOURCE FORMAT IS FREE
       *> gerir_imagens.cbl - CRUD de imagens de produtos
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirImagens.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT img-file ASSIGN TO "dados/produto_imagens.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/produto_imagens.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-prod-status.

       DATA DIVISION.
       FILE SECTION.
       FD img-file.
       01 img-reg.
           05 im-id          PIC 9(6).
           05 im-produto-id  PIC 9(6).
           05 im-caminho     PIC X(200).
           05 im-ordem       PIC 99.

       FD temp-file.
       01 temp-reg.
           05 tl-id          PIC 9(6).
           05 tl-produto-id  PIC 9(6).
           05 tl-caminho     PIC X(200).
           05 tl-ordem       PIC 99.

       FD prod-file.
       01 prod-reg.
           05 pr-id          PIC 9(6).
           05 pr-nome        PIC X(50).
           05 pr-preco       PIC 9(7)V99.
           05 pr-preco-custo PIC 9(7)V99.
           05 pr-stock       PIC 9(6).
           05 pr-margem      PIC 9(3)V99.
           05 pr-ativo       PIC X.
           05 pr-codigo-barras PIC X(14).
           05 pr-categoria   PIC X(20).
           05 pr-sub-categoria PIC X(20).
           05 pr-unidade     PIC X(4).
           05 pr-ncm         PIC X(8).
           05 pr-fornecedor  PIC X(30).
           05 pr-localizacao PIC X(15).
           05 pr-filial-id   PIC 9(3).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(20).
       01 ws-file-status     PIC X(2).
       01 ws-prod-status     PIC X(2).
       01 ws-encontrou       PIC X(1).
       01 ws-json-linha      PIC X(500).
       01 ws-id-ed           PIC Z(6)9.
       01 ws-prod-id-ed      PIC Z(6)9.
       01 ws-total-ed        PIC ZZZ9.
       01 ws-id              PIC 9(6).
       01 ws-produto-id      PIC 9(6).
       01 ws-produto-id-in   PIC X(10).
       01 ws-id-in           PIC X(10).
       01 ws-caminho         PIC X(200).
       01 ws-ordem           PIC 99.
       01 ws-ordem-in        PIC X(3).
       01 ws-prox-id         PIC 9(6).
       01 ws-qtd             PIC 9(4).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "listar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "incluir"  PERFORM incluir
               WHEN "excluir"  PERFORM excluir
               WHEN "listar"   PERFORM listar
               WHEN "listar-por-produto" PERFORM listar-por-produto
               WHEN OTHER      DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       incluir.
           ACCEPT ws-produto-id-in FROM ENVIRONMENT "PRODUTO_ID"
           COMPUTE ws-produto-id = FUNCTION NUMVAL(ws-produto-id-in)
           ACCEPT ws-caminho FROM ENVIRONMENT "CAMINHO"
           ACCEPT ws-ordem-in FROM ENVIRONMENT "ORDEM"
           IF ws-ordem-in NOT = SPACES THEN
               COMPUTE ws-ordem = FUNCTION NUMVAL(ws-ordem-in)
           ELSE MOVE 1 TO ws-ordem END-IF
           IF ws-caminho = SPACES THEN
               DISPLAY "ERRO: caminho da imagem obrigatorio" STOP RUN END-IF
           IF ws-produto-id = 0 THEN
               DISPLAY "ERRO: produto_id obrigatorio" STOP RUN END-IF

           MOVE "N" TO ws-encontrou
           OPEN INPUT prod-file
           IF ws-prod-status NOT = "35" THEN
               PERFORM UNTIL 1 = 2
                   READ prod-file NEXT RECORD
                       AT END EXIT PERFORM
                   END-READ
                   IF pr-id = ws-produto-id AND pr-ativo = "S" THEN
                       MOVE "S" TO ws-encontrou EXIT PERFORM END-IF
               END-PERFORM
           END-IF
           CLOSE prod-file
           IF ws-encontrou = "N" THEN
               DISPLAY "ERRO: produto nao encontrado" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT img-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT img-file CLOSE img-file
               OPEN INPUT img-file END-IF
           PERFORM UNTIL 1 = 2
               READ img-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF im-id > ws-prox-id THEN MOVE im-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE img-file
           ADD 1 TO ws-prox-id

           OPEN EXTEND img-file
           MOVE ws-prox-id TO im-id
           MOVE ws-produto-id TO im-produto-id
           MOVE ws-caminho TO im-caminho
           MOVE ws-ordem TO im-ordem
           WRITE img-reg
           CLOSE img-file
           DISPLAY ws-prox-id.

       excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)

           MOVE "N" TO ws-encontrou
           OPEN INPUT img-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: imagem nao encontrada" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ img-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF im-id NOT = ws-id THEN
                   MOVE im-id TO tl-id
                   MOVE im-produto-id TO tl-produto-id
                   MOVE im-caminho TO tl-caminho
                   MOVE im-ordem TO tl-ordem
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE img-file CLOSE temp-file
           CALL "system" USING "mv dados/produto_imagens.tmp dados/produto_imagens.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: imagem nao encontrada".

       listar.
           OPEN INPUT img-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"imagens":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"imagens":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-prox-id
           PERFORM UNTIL 1 = 2
               READ img-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-prox-id
               IF ws-encontrou = "S" THEN
                   MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE im-id TO ws-id-ed
               MOVE im-produto-id TO ws-prod-id-ed
               MOVE SPACES TO ws-json-linha
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"produto_id":' FUNCTION TRIM(ws-prod-id-ed)
                      ',"caminho":"' FUNCTION TRIM(im-caminho) '"'
                      ',"ordem":' FUNCTION TRIM(im-ordem) '}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-prox-id TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE img-file.

       listar-por-produto.
           ACCEPT ws-produto-id-in FROM ENVIRONMENT "PRODUTO_ID"
           COMPUTE ws-produto-id = FUNCTION NUMVAL(ws-produto-id-in)

           OPEN INPUT img-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"imagens":[],"total":0}'
               STOP RUN END-IF
           MOVE 0 TO ws-qtd
           DISPLAY '{"imagens":['
           MOVE "S" TO ws-encontrou
           PERFORM UNTIL 1 = 2
               READ img-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF im-produto-id = ws-produto-id THEN
                   ADD 1 TO ws-qtd
                   IF ws-encontrou = "S" THEN
                       MOVE "N" TO ws-encontrou
                   ELSE DISPLAY "," END-IF
                   MOVE im-id TO ws-id-ed
                   MOVE SPACES TO ws-json-linha
                   STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                          ',"caminho":"' FUNCTION TRIM(im-caminho) '"'
                          ',"ordem":' FUNCTION TRIM(im-ordem) '}'
                       INTO ws-json-linha
                   DISPLAY FUNCTION TRIM(ws-json-linha)
               END-IF
           END-PERFORM
           MOVE ws-qtd TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE img-file.

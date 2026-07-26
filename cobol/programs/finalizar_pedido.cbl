       >>SOURCE FORMAT IS FREE
       *> finalizar_pedido.cbl - finaliza pedido pendente com pagamento
       IDENTIFICATION DIVISION.
       PROGRAM-ID. FinalizarPedido.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT vendas-file ASSIGN TO "dados/vendas.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/vendas.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD vendas-file.
       01 venda-reg.
           05 vd-id          PIC 9(6).
           05 vd-data        PIC X(10).
           05 vd-hora        PIC X(8).
           05 vd-cliente     PIC X(50).
           05 vd-total       PIC 9(9)V99.
           05 vd-forma-pg    PIC X(15).
           05 vd-filial-id   PIC 9(3).

       FD temp-file.
       01 temp-reg.
           05 tl-id          PIC 9(6).
           05 tl-data        PIC X(10).
           05 tl-hora        PIC X(8).
           05 tl-cliente     PIC X(50).
           05 tl-total       PIC 9(9)V99.
           05 tl-forma-pg    PIC X(15).
           05 tl-filial-id   PIC 9(3).

       WORKING-STORAGE SECTION.
       01 ws-file-status     PIC X(2).
       01 ws-encontrou       PIC X(1).
       01 ws-id              PIC 9(6).
       01 ws-id-in           PIC X(10).
       01 ws-forma-pg        PIC X(15).

       PROCEDURE DIVISION.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-forma-pg FROM ENVIRONMENT "FORMA_PG"
           IF ws-forma-pg = SPACES THEN
               DISPLAY "ERRO: forma_pg obrigatoria" STOP RUN END-IF

           MOVE "N" TO ws-encontrou
           OPEN INPUT vendas-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: venda nao encontrada" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF vd-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE ws-forma-pg TO vd-forma-pg
               END-IF
               MOVE vd-id TO tl-id
               MOVE vd-data TO tl-data
               MOVE vd-hora TO tl-hora
               MOVE vd-cliente TO tl-cliente
               MOVE vd-total TO tl-total
               MOVE vd-forma-pg TO tl-forma-pg
               MOVE vd-filial-id TO tl-filial-id
               WRITE temp-reg
           END-PERFORM
           CLOSE vendas-file CLOSE temp-file
           CALL "system" USING "mv dados/vendas.tmp dados/vendas.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO: venda nao encontrada".

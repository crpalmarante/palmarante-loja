       >>SOURCE FORMAT IS FREE
       *> gerir_numeracao.cbl - Controle de numeracao de notas fiscais
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirNumeracao.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT num-file ASSIGN TO "dados/numeracao.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/numeracao.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD num-file.
       01 num-reg.
           05 nu-ambiente           PIC 9(1).
           05 nu-serie-nfce         PIC 9(3).
           05 nu-prox-num-nfce      PIC 9(9).
           05 nu-serie-nfe          PIC 9(3).
           05 nu-prox-num-nfe       PIC 9(9).

       FD temp-file.
       01 temp-reg.
           05 tu-ambiente           PIC 9(1).
           05 tu-serie-nfce         PIC 9(3).
           05 tu-prox-num-nfce      PIC 9(9).
           05 tu-serie-nfe          PIC 9(3).
           05 tu-prox-num-nfe       PIC 9(9).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-ambiente        PIC 9(1).
       01 ws-amb-in          PIC X(2).
       01 ws-serie-nfce      PIC 9(3).
       01 ws-serie-nfce-in   PIC X(5).
       01 ws-prox-num-nfce   PIC 9(9).
       01 ws-prox-nfce-in    PIC X(10).
       01 ws-serie-nfe       PIC 9(3).
       01 ws-serie-nfe-in    PIC X(5).
       01 ws-prox-num-nfe    PIC 9(9).
       01 ws-prox-nfe-in     PIC X(10).
       01 ws-json            PIC X(300).
       01 ws-amb-dsp         PIC 9.
       01 ws-snfce-dsp       PIC ZZZ.
       01 ws-pnfce-dsp       PIC ZZZZZZZZZ.
       01 ws-snfe-dsp        PIC ZZZ.
       01 ws-pnfe-dsp        PIC ZZZZZZZZZ.

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "mostrar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "gravar"  PERFORM gravar
               WHEN "mostrar" PERFORM mostrar
               WHEN "proximo-nfce" PERFORM proximo-nfce
               WHEN "proximo-nfe"  PERFORM proximo-nfe
               WHEN "avancar-nfce" PERFORM avancar-nfce
               WHEN "avancar-nfe"  PERFORM avancar-nfe
               WHEN OTHER     DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       gravar.
           ACCEPT ws-amb-in FROM ENVIRONMENT "AMBIENTE"
           ACCEPT ws-serie-nfce-in FROM ENVIRONMENT "SERIE_NFCE"
           ACCEPT ws-prox-nfce-in FROM ENVIRONMENT "PROXIMO_NUMERO_NFCE"
           ACCEPT ws-serie-nfe-in FROM ENVIRONMENT "SERIE_NFE"
           ACCEPT ws-prox-nfe-in FROM ENVIRONMENT "PROXIMO_NUMERO_NFE"
           IF ws-amb-in NOT = SPACES THEN
               COMPUTE ws-ambiente = FUNCTION NUMVAL(ws-amb-in) END-IF
           IF ws-serie-nfce-in NOT = SPACES THEN
               COMPUTE ws-serie-nfce = FUNCTION NUMVAL(ws-serie-nfce-in) END-IF
           IF ws-prox-nfce-in NOT = SPACES THEN
               COMPUTE ws-prox-num-nfce = FUNCTION NUMVAL(ws-prox-nfce-in) END-IF
           IF ws-serie-nfe-in NOT = SPACES THEN
               COMPUTE ws-serie-nfe = FUNCTION NUMVAL(ws-serie-nfe-in) END-IF
           IF ws-prox-nfe-in NOT = SPACES THEN
               COMPUTE ws-prox-num-nfe = FUNCTION NUMVAL(ws-prox-nfe-in) END-IF

           OPEN OUTPUT num-file
           MOVE ws-ambiente TO nu-ambiente
           MOVE ws-serie-nfce TO nu-serie-nfce
           MOVE ws-prox-num-nfce TO nu-prox-num-nfce
           MOVE ws-serie-nfe TO nu-serie-nfe
           MOVE ws-prox-num-nfe TO nu-prox-num-nfe
           WRITE num-reg
           CLOSE num-file
           DISPLAY "OK".

       mostrar.
           OPEN INPUT num-file
           IF ws-file-status = "35" THEN
               DISPLAY "{}" STOP RUN END-IF
           READ num-file NEXT RECORD
               AT END
                   DISPLAY "{}" CLOSE num-file STOP RUN
           END-READ
            MOVE nu-ambiente TO ws-amb-dsp
            MOVE nu-serie-nfce TO ws-snfce-dsp
            MOVE nu-prox-num-nfce TO ws-pnfce-dsp
            MOVE nu-serie-nfe TO ws-snfe-dsp
            MOVE nu-prox-num-nfe TO ws-pnfe-dsp
            MOVE SPACES TO ws-json
            STRING '{"ambiente":' FUNCTION TRIM(ws-amb-dsp)
                   ',"serie_nfce":' FUNCTION TRIM(ws-snfce-dsp)
                   ',"proximo_numero_nfce":' FUNCTION TRIM(ws-pnfce-dsp)
                   ',"serie_nfe":' FUNCTION TRIM(ws-snfe-dsp)
                   ',"proximo_numero_nfe":' FUNCTION TRIM(ws-pnfe-dsp) '}'
              INTO ws-json
            DISPLAY FUNCTION TRIM(ws-json)
           CLOSE num-file.

       proximo-nfce.
           OPEN INPUT num-file
           IF ws-file-status = "35" THEN
               DISPLAY "1" STOP RUN END-IF
           READ num-file NEXT RECORD
               AT END
                   DISPLAY "1" CLOSE num-file STOP RUN
           END-READ
           DISPLAY FUNCTION TRIM(nu-prox-num-nfce)
           CLOSE num-file.

       proximo-nfe.
           OPEN INPUT num-file
           IF ws-file-status = "35" THEN
               DISPLAY "1" STOP RUN END-IF
           READ num-file NEXT RECORD
               AT END
                   DISPLAY "1" CLOSE num-file STOP RUN
           END-READ
            DISPLAY FUNCTION TRIM(nu-prox-num-nfe)
            CLOSE num-file.

       avancar-nfce.
           OPEN INPUT num-file
           OPEN OUTPUT temp-file
           IF ws-file-status = "35" THEN
               MOVE 1 TO nu-prox-num-nfce
               MOVE 1 TO nu-ambiente
               MOVE 1 TO nu-serie-nfce
               MOVE 1 TO nu-serie-nfe
               MOVE 1 TO nu-prox-num-nfe
               DISPLAY 1
               WRITE temp-reg
               CLOSE num-file CLOSE temp-file
               STOP RUN
           END-IF
           READ num-file NEXT RECORD
               AT END
                   MOVE 1 TO nu-prox-num-nfce
                   DISPLAY "1"
                   CLOSE num-file CLOSE temp-file
                   STOP RUN
           END-READ
           MOVE nu-ambiente TO tu-ambiente
           MOVE nu-serie-nfce TO tu-serie-nfce
           MOVE nu-prox-num-nfce TO tu-prox-num-nfce
           MOVE nu-serie-nfe TO tu-serie-nfe
           MOVE nu-prox-num-nfe TO tu-prox-num-nfe
           DISPLAY FUNCTION TRIM(tu-prox-num-nfce)
           ADD 1 TO tu-prox-num-nfce
           WRITE temp-reg
           CLOSE num-file CLOSE temp-file
           CALL "system" USING "mv dados/numeracao.tmp dados/numeracao.dat"
           END-CALL.

       avancar-nfe.
           OPEN INPUT num-file
           OPEN OUTPUT temp-file
           IF ws-file-status = "35" THEN
               MOVE 1 TO nu-prox-num-nfe
               MOVE 1 TO nu-ambiente
               MOVE 1 TO nu-serie-nfce
               MOVE 1 TO nu-serie-nfe
               MOVE 1 TO nu-prox-num-nfce
               DISPLAY 1
               WRITE temp-reg
               CLOSE num-file CLOSE temp-file
               STOP RUN
           END-IF
           READ num-file NEXT RECORD
               AT END
                   MOVE 1 TO nu-prox-num-nfe
                   DISPLAY "1"
                   CLOSE num-file CLOSE temp-file
                   STOP RUN
           END-READ
           MOVE nu-ambiente TO tu-ambiente
           MOVE nu-serie-nfce TO tu-serie-nfce
           MOVE nu-prox-num-nfce TO tu-prox-num-nfce
           MOVE nu-serie-nfe TO tu-serie-nfe
           MOVE nu-prox-num-nfe TO tu-prox-num-nfe
           DISPLAY FUNCTION TRIM(tu-prox-num-nfe)
           ADD 1 TO tu-prox-num-nfe
           WRITE temp-reg
           CLOSE num-file CLOSE temp-file
           CALL "system" USING "mv dados/numeracao.tmp dados/numeracao.dat"
           END-CALL.

       >>SOURCE FORMAT IS FREE
       *> batch_json_numeracao.cbl - Numeracao .dat -> .json
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BatchJSONNumeracao.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT num-file ASSIGN TO "dados/numeracao.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT json-file ASSIGN TO "dados/numeracao.json"
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

       FD json-file.
       01 json-line PIC X(500).

       WORKING-STORAGE SECTION.
       01 ws-file-status PIC X(2).
       01 ws-amb-ed     PIC 9.
       01 ws-snfce-ed   PIC ZZZ.
       01 ws-pnfce-ed   PIC ZZZZZZZZZ.
       01 ws-snfe-ed    PIC ZZZ.
       01 ws-pnfe-ed    PIC ZZZZZZZZZ.

       PROCEDURE DIVISION.
           OPEN OUTPUT json-file
           OPEN INPUT num-file
           IF ws-file-status NOT = "35" THEN
               READ num-file NEXT RECORD
                   AT END
                       MOVE SPACES TO json-line
                       STRING '{"ambiente":2,"serie_nfce":1,"proximo_numero_nfce":1,"serie_nfe":1,"proximo_numero_nfe":1}'
                         INTO json-line
                       WRITE json-line
                       CLOSE num-file CLOSE json-file
                       DISPLAY "JSON numeracao gerado (default)"
                       STOP RUN
               END-READ
               MOVE nu-ambiente TO ws-amb-ed
               MOVE nu-serie-nfce TO ws-snfce-ed
               MOVE nu-prox-num-nfce TO ws-pnfce-ed
               MOVE nu-serie-nfe TO ws-snfe-ed
               MOVE nu-prox-num-nfe TO ws-pnfe-ed
               MOVE SPACES TO json-line
               STRING '{"ambiente":' FUNCTION TRIM(ws-amb-ed)
                      ',"serie_nfce":' FUNCTION TRIM(ws-snfce-ed)
                      ',"proximo_numero_nfce":' FUNCTION TRIM(ws-pnfce-ed)
                      ',"serie_nfe":' FUNCTION TRIM(ws-snfe-ed)
                      ',"proximo_numero_nfe":' FUNCTION TRIM(ws-pnfe-ed) '}'
                 INTO json-line
               WRITE json-line
               CLOSE num-file CLOSE json-file
               DISPLAY "JSON numeracao gerado"
           ELSE
               MOVE SPACES TO json-line
               STRING '{"ambiente":2,"serie_nfce":1,"proximo_numero_nfce":1,"serie_nfe":1,"proximo_numero_nfe":1}'
                 INTO json-line
               WRITE json-line
               CLOSE json-file
               DISPLAY "JSON numeracao gerado (default)"
           END-IF.

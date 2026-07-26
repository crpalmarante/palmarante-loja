       >>SOURCE FORMAT IS FREE
       *> batch_json_fornecedores.cbl - Fornecedores .dat -> .json
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BatchJSONFornecedores.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT forn-file ASSIGN TO "dados/fornecedores.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.

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

       WORKING-STORAGE SECTION.
       01 ws-file-status     PIC X(2).
       01 ws-json-linha      PIC X(500).
       01 ws-id-ed           PIC ZZZZ9.
       01 ws-total-ed        PIC ZZZZ9.
       01 ws-total           PIC 9(5).
       01 ws-i               PIC 9(5).
       01 ws-qtd-arq         PIC 9(5).
       01 ws-existe          PIC X(1).

       PROCEDURE DIVISION.
           OPEN INPUT forn-file
           IF ws-file-status = "35" THEN
               DISPLAY "JSON fornecedores gerado: 0 fornecedores"
               STOP RUN END-IF

           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
           END-PERFORM
           CLOSE forn-file

           IF ws-total = 0 THEN
               DISPLAY "JSON fornecedores gerado: 0 fornecedores"
               STOP RUN END-IF

           OPEN INPUT forn-file
           DISPLAY '{"fornecedores":['
           MOVE "S" TO ws-existe
           MOVE 0 TO ws-i
           PERFORM UNTIL 1 = 2
               READ forn-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-i
               IF ws-existe = "S" THEN
                   MOVE "N" TO ws-existe
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
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE forn-file.
           DISPLAY "JSON fornecedores gerado: " FUNCTION TRIM(ws-total-ed) " fornecedores"
           STOP RUN.

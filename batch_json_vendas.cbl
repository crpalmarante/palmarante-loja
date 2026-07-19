       >>SOURCE FORMAT IS FREE
       *> batch_json_vendas.cbl - Vendas .dat -> .json
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BatchJSONVendas.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT vendas-file ASSIGN TO "dados/vendas.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT itens-file ASSIGN TO "dados/itens_venda.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT json-file ASSIGN TO "dados/vendas.json"
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
            05 vd-filial-id       PIC 9(3).

        FD itens-file.
       01 item-reg.
           05 iv-venda-id    PIC 9(6).
           05 iv-item        PIC 9(3).
           05 iv-prod-id     PIC 9(6).
           05 iv-prod-nome   PIC X(50).
           05 iv-qtd         PIC 9(4).
           05 iv-preco-uni   PIC 9(7)V99.
            05 iv-subtotal    PIC 9(9)V99.
            05 iv-filial-id       PIC 9(3).

        FD json-file.
       01 json-line PIC X(600).

       WORKING-STORAGE SECTION.
       01 ws-primeiro         PIC X(1) VALUE "S".
       01 ws-item-primeiro    PIC X(1).
       01 ws-total-ed         PIC ZZZZZZZ.99.
       01 ws-id-ed            PIC ZZZZZ9.
       01 ws-qtd-ed           PIC ZZZ9.
       01 ws-preco-ed         PIC ZZZZZZZ.99.
       01 ws-sub-ed           PIC ZZZZZZZZZ.99.
       01 ws-prod-id-ed       PIC ZZZZZ9.
       01 ws-total-vendas     PIC 9(4).
       01 ws-total-qtd-ed     PIC ZZZ9.
        01 ws-id-atual         PIC 9(6).
        01 ws-filial-ed        PIC ZZ9.

        PROCEDURE DIVISION.
           OPEN INPUT vendas-file
           OPEN INPUT itens-file
           OPEN OUTPUT json-file

           MOVE 0 TO ws-total-vendas
           MOVE SPACES TO json-line
           STRING '{"vendas":[' INTO json-line
           WRITE json-line

           PERFORM UNTIL 1 = 2
               READ vendas-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ

               ADD 1 TO ws-total-vendas
               MOVE vd-id TO ws-id-ed
               MOVE vd-total TO ws-total-ed

               IF ws-primeiro = "S"
                   MOVE "N" TO ws-primeiro
               ELSE
                   MOVE SPACES TO json-line
                   STRING "," INTO json-line
                   WRITE json-line
               END-IF

                MOVE vd-filial-id TO ws-filial-ed
                MOVE SPACES TO json-line
                STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                       ',"data":"' FUNCTION TRIM(vd-data) '"'
                       ',"hora":"' FUNCTION TRIM(vd-hora) '"'
                       ',"cliente":"' FUNCTION TRIM(vd-cliente) '"'
                       ',"total":' FUNCTION TRIM(ws-total-ed)
                       ',"forma_pg":"' FUNCTION TRIM(vd-forma-pg) '"'
                       ',"filial_id":' FUNCTION TRIM(ws-filial-ed)
                       ',"itens":['
                   INTO json-line
               WRITE json-line

               MOVE "S" TO ws-item-primeiro
               MOVE vd-id TO ws-id-atual
               PERFORM UNTIL 1 = 2
                   READ itens-file NEXT RECORD
                       AT END EXIT PERFORM
                   END-READ
                   IF iv-venda-id = ws-id-atual THEN
                       MOVE iv-qtd TO ws-qtd-ed
                       MOVE iv-preco-uni TO ws-preco-ed
                       MOVE iv-subtotal TO ws-sub-ed
                       IF ws-item-primeiro = "S"
                           MOVE "N" TO ws-item-primeiro
                       ELSE
                           MOVE SPACES TO json-line
                           STRING "," INTO json-line
                           WRITE json-line
                       END-IF
                         MOVE iv-filial-id TO ws-filial-ed
                         MOVE iv-prod-id TO ws-prod-id-ed
                         MOVE SPACES TO json-line
                         STRING '{"prod_id":' FUNCTION TRIM(ws-prod-id-ed)
                                ',"produto":"' FUNCTION TRIM(iv-prod-nome) '"'
                               ',"qtd":' FUNCTION TRIM(ws-qtd-ed)
                               ',"preco":' FUNCTION TRIM(ws-preco-ed)
                               ',"subtotal":' FUNCTION TRIM(ws-sub-ed)
                               ',"filial_id":' FUNCTION TRIM(ws-filial-ed) '}'
                           INTO json-line
                       WRITE json-line
                   END-IF
               END-PERFORM
               CLOSE itens-file
               OPEN INPUT itens-file

               MOVE SPACES TO json-line
               STRING ']}' INTO json-line
               WRITE json-line
           END-PERFORM

            MOVE ws-total-vendas TO ws-total-qtd-ed
            MOVE SPACES TO json-line
            STRING '],"total_vendas":' FUNCTION TRIM(ws-total-qtd-ed) '}' INTO json-line
            WRITE json-line

           CLOSE vendas-file
           CLOSE itens-file
           CLOSE json-file
           DISPLAY "JSON vendas gerado: " ws-total-vendas " vendas".

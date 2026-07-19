       >>SOURCE FORMAT IS FREE
       *> batch_json_produtos.cbl - Produtos .dat -> .json
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BatchJSONProdutos.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT prod-file ASSIGN TO "dados/produtos.dat"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT json-file ASSIGN TO "dados/produtos.json"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD prod-file.
       01 prod-reg.
           05 pr-id              PIC 9(6).
           05 pr-nome            PIC X(50).
           05 pr-preco           PIC 9(7)V99.
           05 pr-preco-custo     PIC 9(7)V99.
           05 pr-stock           PIC 9(6).
           05 pr-margem          PIC 9(3)V99.
           05 pr-ativo           PIC X(1).
           05 pr-codigo-barras   PIC X(14).
            05 pr-categoria       PIC X(20).
            05 pr-sub-categoria   PIC X(20).
            05 pr-unidade         PIC X(4).
           05 pr-ncm             PIC X(8).
            05 pr-fornecedor      PIC X(30).
            05 pr-localizacao     PIC X(15).
             05 pr-filial-id       PIC 9(3).
             05 pr-cst            PIC X(3).
             05 pr-cfop           PIC X(4).
             05 pr-icms-alq       PIC 9(3)V99.
             05 pr-servico        PIC X(1).
             05 pr-iss-alq        PIC 9(3)V99.
             05 pr-cod-serv-mun   PIC X(20).

        FD json-file.
       01 json-line PIC X(800).

       WORKING-STORAGE SECTION.
       01 ws-primeiro         PIC X(1) VALUE "S".
       01 ws-preco-ed         PIC ZZZZZZZ.99.
       01 ws-custo-ed         PIC ZZZZZZZ.99.
       01 ws-margem-ed        PIC ZZZ.99.
       01 ws-id-ed            PIC ZZZZZ9.
       01 ws-stock-ed         PIC ZZZZZ9.
        01 ws-filial-ed        PIC ZZ9.
        01 ws-icms-ed          PIC ZZZ.99.
        01 ws-total            PIC 9(4).

       PROCEDURE DIVISION.
           OPEN INPUT prod-file
           OPEN OUTPUT json-file

           MOVE 0 TO ws-total
           MOVE SPACES TO json-line
           STRING '{"produtos":[' INTO json-line
           WRITE json-line

           PERFORM UNTIL 1 = 2
               READ prod-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ

               IF pr-ativo NOT = "S" THEN EXIT PERFORM CYCLE END-IF

               ADD 1 TO ws-total
               MOVE pr-id TO ws-id-ed
               MOVE pr-preco TO ws-preco-ed
               MOVE pr-preco-custo TO ws-custo-ed
               MOVE pr-stock TO ws-stock-ed
               MOVE pr-margem TO ws-margem-ed
                MOVE pr-filial-id TO ws-filial-ed
                MOVE pr-icms-alq TO ws-icms-ed

               IF ws-primeiro = "S"
                   MOVE "N" TO ws-primeiro
               ELSE
                   MOVE SPACES TO json-line
                   STRING "," INTO json-line
                   WRITE json-line
               END-IF

               MOVE SPACES TO json-line
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                      ',"nome":"' FUNCTION TRIM(pr-nome) '"'
                      ',"preco":' FUNCTION TRIM(ws-preco-ed)
                      ',"preco_custo":' FUNCTION TRIM(ws-custo-ed)
                      ',"stock":' FUNCTION TRIM(ws-stock-ed)
                      ',"margem":' FUNCTION TRIM(ws-margem-ed)
                      ',"codigo_barras":"' FUNCTION TRIM(pr-codigo-barras) '"'
                      ',"categoria":"' FUNCTION TRIM(pr-categoria) '"'
                      ',"sub_categoria":"' FUNCTION TRIM(pr-sub-categoria) '"'
                      ',"unidade":"' FUNCTION TRIM(pr-unidade) '"'
                      ',"ncm":"' FUNCTION TRIM(pr-ncm) '"'
                      ',"fornecedor":"' FUNCTION TRIM(pr-fornecedor) '"'
                      ',"localizacao":"' FUNCTION TRIM(pr-localizacao) '"'
                       ',"filial_id":' FUNCTION TRIM(ws-filial-ed)
                       ',"cst":"' FUNCTION TRIM(pr-cst) '"'
                       ',"cfop":"' FUNCTION TRIM(pr-cfop) '"'
                        ',"icms_alq":' FUNCTION TRIM(ws-icms-ed)
                        ',"servico":"' FUNCTION TRIM(pr-servico) '"'
                        ',"iss_alq":' FUNCTION TRIM(ws-margem-ed)
                        ',"cod_serv_mun":"' FUNCTION TRIM(pr-cod-serv-mun) '"'
                        '}'
                   INTO json-line
               WRITE json-line
           END-PERFORM

           MOVE ws-total TO ws-id-ed
           MOVE SPACES TO json-line
           STRING '],"total":' FUNCTION TRIM(ws-id-ed) '}' INTO json-line
           WRITE json-line

           CLOSE prod-file
           CLOSE json-file
           DISPLAY "JSON produtos gerado: " ws-total " produtos".

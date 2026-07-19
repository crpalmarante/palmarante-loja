       >>SOURCE FORMAT IS FREE
       *> gerir_empresa.cbl - Configuracao global da empresa
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GerirEmpresa.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT emp-file ASSIGN TO "dados/empresa.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.

       DATA DIVISION.
       FILE SECTION.
       FD emp-file.
       01 emp-reg.
           05 em-nome             PIC X(50).
           05 em-cnpj             PIC X(18).
           05 em-endereco         PIC X(50).
           05 em-telefone         PIC X(15).
           05 em-email            PIC X(40).
           05 em-certificado      PIC X(100).
           05 em-cert-senha       PIC X(50).
           05 em-cnpj-status      PIC X(1).
           05 em-inscricao-est    PIC X(20).
            05 em-logo             PIC X(100).
            05 em-cnae-prim-codigo PIC X(10).
            05 em-cnae-prim-desc   PIC X(80).
            05 em-cnae-sec-codigos PIC X(100).
            05 em-cnae-sec-desc    PIC X(200).
             05 em-tipo-fiscal      PIC X(20).
              05 em-chave-pix        PIC X(50).
              05 em-crt             PIC 9(1).
              05 em-cod-municipio   PIC X(7).
               05 em-inscricao-mun   PIC X(20).
               05 em-uf             PIC 9(2).

       WORKING-STORAGE SECTION.
       01 ws-acao            PIC X(15).
       01 ws-file-status     PIC X(2).
       01 ws-nome            PIC X(50).
       01 ws-cnpj            PIC X(18).
       01 ws-endereco        PIC X(50).
       01 ws-telefone        PIC X(15).
       01 ws-email           PIC X(40).
       01 ws-certificado     PIC X(100).
       01 ws-cert-senha      PIC X(50).
       01 ws-cnpj-status     PIC X(1).
       01 ws-inscricao-est   PIC X(20).
        01 ws-logo            PIC X(100).
        01 ws-cnae-prim-codigo  PIC X(10).
        01 ws-cnae-prim-desc    PIC X(80).
        01 ws-cnae-sec-codigos  PIC X(100).
        01 ws-cnae-sec-desc     PIC X(200).
       01 ws-tipo-fiscal     PIC X(20).
        01 ws-chave-pix       PIC X(50).
        01 ws-crt             PIC 9(1).
        01 ws-crt-in          PIC X(2).
        01 ws-cod-municipio   PIC X(7).
         01 ws-inscricao-mun   PIC X(20).
         01 ws-uf             PIC X(2).
        01 ws-json            PIC X(1800).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "mostrar" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "gravar"  PERFORM gravar
               WHEN "mostrar" PERFORM mostrar
               WHEN OTHER     DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       gravar.
           ACCEPT ws-nome FROM ENVIRONMENT "NOME"
           ACCEPT ws-cnpj FROM ENVIRONMENT "CNPJ"
           ACCEPT ws-endereco FROM ENVIRONMENT "ENDERECO"
           ACCEPT ws-telefone FROM ENVIRONMENT "TELEFONE"
           ACCEPT ws-email FROM ENVIRONMENT "EMAIL"
           ACCEPT ws-certificado FROM ENVIRONMENT "CERTIFICADO"
           ACCEPT ws-cert-senha FROM ENVIRONMENT "CERT_SENHA"
           ACCEPT ws-cnpj-status FROM ENVIRONMENT "CNPJ_STATUS"
           ACCEPT ws-inscricao-est FROM ENVIRONMENT "INSCRICAO_EST"
            ACCEPT ws-logo FROM ENVIRONMENT "LOGO"
            ACCEPT ws-cnae-prim-codigo FROM ENVIRONMENT "CNAE_PRIM_CODIGO"
            ACCEPT ws-cnae-prim-desc FROM ENVIRONMENT "CNAE_PRIM_DESC"
            ACCEPT ws-cnae-sec-codigos FROM ENVIRONMENT "CNAE_SEC_CODIGOS"
            ACCEPT ws-cnae-sec-desc FROM ENVIRONMENT "CNAE_SEC_DESC"
             ACCEPT ws-tipo-fiscal FROM ENVIRONMENT "TIPO_FISCAL"
              ACCEPT ws-chave-pix FROM ENVIRONMENT "CHAVE_PIX"
              ACCEPT ws-crt-in FROM ENVIRONMENT "CRT"
              IF ws-crt-in NOT = SPACES THEN
                  COMPUTE ws-crt = FUNCTION NUMVAL(ws-crt-in) END-IF
               ACCEPT ws-cod-municipio FROM ENVIRONMENT "COD_MUNICIPIO"
               ACCEPT ws-inscricao-mun FROM ENVIRONMENT "INSCRICAO_MUN"
               ACCEPT ws-uf FROM ENVIRONMENT "UF"
               IF ws-uf = SPACES THEN MOVE "43" TO ws-uf END-IF
             IF ws-nome = SPACES THEN
               DISPLAY "ERRO: nome obrigatorio" STOP RUN END-IF

           OPEN OUTPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO: nao foi possivel criar empresa.dat"
               STOP RUN END-IF
           MOVE ws-nome TO em-nome
           MOVE ws-cnpj TO em-cnpj
           MOVE ws-endereco TO em-endereco
           MOVE ws-telefone TO em-telefone
           MOVE ws-email TO em-email
           MOVE ws-certificado TO em-certificado
           MOVE ws-cert-senha TO em-cert-senha
           MOVE ws-cnpj-status TO em-cnpj-status
           MOVE ws-inscricao-est TO em-inscricao-est
            MOVE ws-logo TO em-logo
            MOVE ws-cnae-prim-codigo TO em-cnae-prim-codigo
            MOVE ws-cnae-prim-desc TO em-cnae-prim-desc
            MOVE ws-cnae-sec-codigos TO em-cnae-sec-codigos
            MOVE ws-cnae-sec-desc TO em-cnae-sec-desc
             MOVE ws-tipo-fiscal TO em-tipo-fiscal
              MOVE ws-chave-pix TO em-chave-pix
              MOVE ws-crt TO em-crt
               MOVE ws-cod-municipio TO em-cod-municipio
               MOVE ws-inscricao-mun TO em-inscricao-mun
               MOVE FUNCTION NUMVAL(ws-uf) TO em-uf
              WRITE emp-reg
           CLOSE emp-file
           DISPLAY "OK".

       mostrar.
           OPEN INPUT emp-file
           IF ws-file-status = "35" THEN
               DISPLAY "{}"
               STOP RUN END-IF
           READ emp-file NEXT RECORD
               AT END
                   DISPLAY "{}"
                   CLOSE emp-file
                   STOP RUN
           END-READ
           MOVE SPACES TO ws-json
           STRING '{"nome":"' FUNCTION TRIM(em-nome)
                  '","cnpj":"'  FUNCTION TRIM(em-cnpj)
                  '","endereco":"' FUNCTION TRIM(em-endereco)
                  '","telefone":"' FUNCTION TRIM(em-telefone)
                  '","email":"' FUNCTION TRIM(em-email)
                  '","certificado":"' FUNCTION TRIM(em-certificado)
                  '","cert_senha":"' FUNCTION TRIM(em-cert-senha)
                  '","cnpj_status":"' FUNCTION TRIM(em-cnpj-status)
                  '","inscricao_est":"' FUNCTION TRIM(em-inscricao-est)
                   '","logo":"' FUNCTION TRIM(em-logo)
                   '","cnae_prim_codigo":"' FUNCTION TRIM(em-cnae-prim-codigo)
                   '","cnae_prim_desc":"' FUNCTION TRIM(em-cnae-prim-desc)
                   '","cnae_sec_codigos":"' FUNCTION TRIM(em-cnae-sec-codigos)
                   '","cnae_sec_desc":"' FUNCTION TRIM(em-cnae-sec-desc)
                    '","tipo_fiscal":"' FUNCTION TRIM(em-tipo-fiscal)
                     '","chave_pix":"' FUNCTION TRIM(em-chave-pix)
                     '","crt":' FUNCTION TRIM(em-crt)
                     ',"cod_municipio":"' FUNCTION TRIM(em-cod-municipio)
                      '","inscricao_mun":"' FUNCTION TRIM(em-inscricao-mun)
                      '","uf":' FUNCTION TRIM(em-uf) '}'
                   INTO ws-json
           DISPLAY FUNCTION TRIM(ws-json)
           CLOSE emp-file.

       >>SOURCE FORMAT IS FREE
       *> folha_pagamento.cbl - Folha de pagamento (payroll)
       IDENTIFICATION DIVISION.
       PROGRAM-ID. FolhaPagamento.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT cf-file ASSIGN TO "dados/folha_config.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT hl-file ASSIGN TO "dados/holerites.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT temp-file ASSIGN TO "dados/holerites.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT fe-file ASSIGN TO "dados/ferias.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT fe-temp ASSIGN TO "dados/ferias.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT de-file ASSIGN TO "dados/decimo.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT de-temp ASSIGN TO "dados/decimo.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT re-file ASSIGN TO "dados/rescisoes.dat"
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS ws-file-status.
           SELECT re-temp ASSIGN TO "dados/rescisoes.tmp"
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD cf-file.
       01 cf-reg.
           05 cf-salario-minimo    PIC 9(7)V99.
           05 cf-inss-f1-teto      PIC 9(6)V99.
           05 cf-inss-f1-aliq      PIC 9(3)V99.
           05 cf-inss-f2-teto      PIC 9(6)V99.
           05 cf-inss-f2-aliq      PIC 9(3)V99.
           05 cf-inss-f3-teto      PIC 9(6)V99.
           05 cf-inss-f3-aliq      PIC 9(3)V99.
           05 cf-inss-f4-teto      PIC 9(6)V99.
           05 cf-inss-f4-aliq      PIC 9(3)V99.
           05 cf-irrf-ded-dep      PIC 9(5)V99.
           05 cf-irrf-f1-teto      PIC 9(6)V99.
           05 cf-irrf-f1-aliq      PIC 9(3)V99.
           05 cf-irrf-f2-teto      PIC 9(6)V99.
           05 cf-irrf-f2-aliq      PIC 9(3)V99.
           05 cf-irrf-f3-teto      PIC 9(6)V99.
           05 cf-irrf-f3-aliq      PIC 9(3)V99.
           05 cf-irrf-f4-teto      PIC 9(6)V99.
           05 cf-irrf-f4-aliq      PIC 9(3)V99.
           05 cf-fgts-aliquota     PIC 9(3)V99.
           05 cf-hora-extra-aliq   PIC 9(3)V99.

       FD hl-file.
       01 hl-reg.
           05 hl-id                PIC 9(4).
           05 hl-func-id           PIC 9(3).
           05 hl-nome              PIC X(50).
           05 hl-competencia       PIC X(7).
           05 hl-salario-base      PIC 9(7)V99.
           05 hl-horas-extras      PIC 9(3)V99.
           05 hl-valor-hora-extra  PIC 9(5)V99.
           05 hl-dsr               PIC 9(7)V99.
           05 hl-faltas-dias       PIC 9(2).
           05 hl-proventos         PIC 9(8)V99.
           05 hl-inss              PIC 9(7)V99.
           05 hl-irrf              PIC 9(7)V99.
           05 hl-fgts              PIC 9(7)V99.
           05 hl-outros-desc       PIC 9(7)V99.
           05 hl-total-desc        PIC 9(8)V99.
           05 hl-liquido           PIC 9(8)V99.
           05 hl-situacao          PIC X.
           05 hl-data-pagamento    PIC X(10).

       FD temp-file.
       01 temp-reg.
           05 tl-id                PIC 9(4).
           05 tl-func-id           PIC 9(3).
           05 tl-nome              PIC X(50).
           05 tl-competencia       PIC X(7).
           05 tl-salario-base      PIC 9(7)V99.
           05 tl-horas-extras      PIC 9(3)V99.
           05 tl-valor-hora-extra  PIC 9(5)V99.
           05 tl-dsr               PIC 9(7)V99.
           05 tl-faltas-dias       PIC 9(2).
           05 tl-proventos         PIC 9(8)V99.
           05 tl-inss              PIC 9(7)V99.
           05 tl-irrf              PIC 9(7)V99.
           05 tl-fgts              PIC 9(7)V99.
           05 tl-outros-desc       PIC 9(7)V99.
           05 tl-total-desc        PIC 9(8)V99.
           05 tl-liquido           PIC 9(8)V99.
           05 tl-situacao          PIC X.
           05 tl-data-pagamento    PIC X(10).

       FD fe-file.
       01 fe-reg.
           05 fe-id                PIC 9(4).
           05 fe-funcionario-id    PIC 9(3).
           05 fe-nome              PIC X(50).
           05 fe-aquis-inicio      PIC X(10).
           05 fe-aquis-fim         PIC X(10).
           05 fe-inicio            PIC X(10).
           05 fe-fim               PIC X(10).
           05 fe-dias              PIC 9(2).
           05 fe-dias-abono        PIC 9(2).
           05 fe-valor-base        PIC 9(7)V99.
           05 fe-1-3               PIC 9(7)V99.
           05 fe-abono             PIC 9(7)V99.
           05 fe-abono-1-3         PIC 9(7)V99.
           05 fe-inss              PIC 9(7)V99.
           05 fe-irrf              PIC 9(7)V99.
           05 fe-liquido           PIC 9(8)V99.
           05 fe-situacao          PIC X.
           05 fe-data-pagamento    PIC X(10).

       FD fe-temp.
       01 fe-temp-reg.
           05 te-id                PIC 9(4).
           05 te-funcionario-id    PIC 9(3).
           05 te-nome              PIC X(50).
           05 te-aquis-inicio      PIC X(10).
           05 te-aquis-fim         PIC X(10).
           05 te-inicio            PIC X(10).
           05 te-fim               PIC X(10).
           05 te-dias              PIC 9(2).
           05 te-dias-abono        PIC 9(2).
           05 te-valor-base        PIC 9(7)V99.
           05 te-1-3               PIC 9(7)V99.
           05 te-abono             PIC 9(7)V99.
           05 te-abono-1-3         PIC 9(7)V99.
           05 te-inss              PIC 9(7)V99.
           05 te-irrf              PIC 9(7)V99.
           05 te-liquido           PIC 9(8)V99.
           05 te-situacao          PIC X.
           05 te-data-pagamento    PIC X(10).

       FD de-file.
       01 de-reg.
           05 de-id                PIC 9(4).
           05 de-funcionario-id    PIC 9(3).
           05 de-nome              PIC X(50).
           05 de-ano               PIC X(4).
           05 de-parcela           PIC X(1).
           05 de-valor-base        PIC 9(7)V99.
           05 de-inss              PIC 9(7)V99.
           05 de-irrf              PIC 9(7)V99.
           05 de-liquido           PIC 9(8)V99.
           05 de-situacao          PIC X.
           05 de-data-pagamento    PIC X(10).

       FD de-temp.
       01 de-temp-reg.
           05 qe-id                PIC 9(4).
           05 qe-funcionario-id    PIC 9(3).
           05 qe-nome              PIC X(50).
           05 qe-ano               PIC X(4).
           05 qe-parcela           PIC X(1).
           05 qe-valor-base        PIC 9(7)V99.
           05 qe-inss              PIC 9(7)V99.
           05 qe-irrf              PIC 9(7)V99.
           05 qe-liquido           PIC 9(8)V99.
           05 qe-situacao          PIC X.
           05 qe-data-pagamento    PIC X(10).

       FD re-file.
       01 re-reg.
           05 re-id                PIC 9(4).
           05 re-funcionario-id    PIC 9(3).
           05 re-nome              PIC X(50).
           05 re-data-deslig       PIC X(10).
           05 re-tipo-aviso        PIC X(20).
           05 re-dias-aviso        PIC 9(2).
           05 re-saldo-salario     PIC 9(7)V99.
           05 re-ferias-venc       PIC 9(7)V99.
           05 re-ferias-prop       PIC 9(7)V99.
           05 re-1-3-ferias        PIC 9(7)V99.
           05 re-13-prop           PIC 9(7)V99.
           05 re-fgts              PIC 9(7)V99.
           05 re-multa-fgts        PIC 9(7)V99.
           05 re-inss              PIC 9(7)V99.
           05 re-irrf              PIC 9(7)V99.
           05 re-liquido           PIC 9(8)V99.
           05 re-situacao          PIC X.
           05 re-data-pagamento    PIC X(10).

       FD re-temp.
       01 re-temp-reg.
           05 se-id                PIC 9(4).
           05 se-funcionario-id    PIC 9(3).
           05 se-nome              PIC X(50).
           05 se-data-deslig       PIC X(10).
           05 se-tipo-aviso        PIC X(20).
           05 se-dias-aviso        PIC 9(2).
           05 se-saldo-salario     PIC 9(7)V99.
           05 se-ferias-venc       PIC 9(7)V99.
           05 se-ferias-prop       PIC 9(7)V99.
           05 se-1-3-ferias        PIC 9(7)V99.
           05 se-13-prop           PIC 9(7)V99.
           05 se-fgts              PIC 9(7)V99.
           05 se-multa-fgts        PIC 9(7)V99.
           05 se-inss              PIC 9(7)V99.
           05 se-irrf              PIC 9(7)V99.
           05 se-liquido           PIC 9(8)V99.
           05 se-situacao          PIC X.
           05 se-data-pagamento    PIC X(10).

       WORKING-STORAGE SECTION.
       01 ws-acao              PIC X(20).
       01 ws-file-status       PIC X(2).
       01 ws-encontrou         PIC X.
       01 ws-prox-id           PIC 9(4).
       01 ws-total             PIC 9(4).
       01 ws-total-ed          PIC Z(3)9.
       01 ws-id-ed             PIC Z(3)9.
       01 ws-func-id-ed        PIC Z(3)9.
       01 ws-ed                PIC -(9)9.99.
       01 ws-ne                PIC -(7)9.99.
       01 ws-je                PIC Z(7)9.99.
       01 ws-json-linha        PIC X(1500).
       01 ws-id-in             PIC X(5).
       01 ws-id                PIC 9(4).
       01 ws-func-id           PIC 9(3).
       01 ws-func-id-in        PIC X(5).
       01 ws-valor-in          PIC X(12).
       01 ws-horas-in          PIC X(6).
       01 ws-data-in           PIC X(10).
       01 ws-faltas-in         PIC X(3).
       01 ws-nome-in           PIC X(50).
       01 ws-dias-in           PIC X(3).
       01 ws-ano-in            PIC X(4).
       01 ws-parcela-in        PIC X(1).
       01 ws-tipo-aviso-in     PIC X(20).

       PROCEDURE DIVISION.
           ACCEPT ws-acao FROM ENVIRONMENT "ACAO"
           IF ws-acao = SPACES THEN MOVE "config-ler" TO ws-acao END-IF

           EVALUATE ws-acao
               WHEN "config-ler"         PERFORM config-ler
               WHEN "config-salvar"      PERFORM config-salvar
               WHEN "holerite-gerar"     PERFORM holerite-gerar
               WHEN "holerite-listar"    PERFORM holerite-listar
               WHEN "holerite-pagar"     PERFORM holerite-pagar
               WHEN "holerite-excluir"   PERFORM holerite-excluir
               WHEN "ferias-incluir"     PERFORM ferias-incluir
               WHEN "ferias-listar"      PERFORM ferias-listar
               WHEN "ferias-pagar"       PERFORM ferias-pagar
               WHEN "ferias-excluir"     PERFORM ferias-excluir
               WHEN "decimo-incluir"     PERFORM decimo-incluir
               WHEN "decimo-listar"      PERFORM decimo-listar
               WHEN "decimo-pagar"       PERFORM decimo-pagar
               WHEN "decimo-excluir"     PERFORM decimo-excluir
               WHEN "rescisao-incluir"   PERFORM rescisao-incluir
               WHEN "rescisao-listar"    PERFORM rescisao-listar
               WHEN "rescisao-pagar"     PERFORM rescisao-pagar
               WHEN "rescisao-excluir"   PERFORM rescisao-excluir
               WHEN OTHER DISPLAY "ERRO: acao invalida"
           END-EVALUATE
           STOP RUN.

       config-ler.
           OPEN INPUT cf-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"salario_minimo":1412.00,"inss_f1_teto":1412.00,"inss_f1_aliq":7.50,"inss_f2_teto":2666.68,"inss_f2_aliq":9.00,"inss_f3_teto":4000.03,"inss_f3_aliq":12.00,"inss_f4_teto":7786.02,"inss_f4_aliq":14.00,"irrf_ded_dep":189.59,"irrf_f1_teto":2112.00,"irrf_f1_aliq":0.00,"irrf_f2_teto":2826.65,"irrf_f2_aliq":7.50,"irrf_f3_teto":3751.05,"irrf_f3_aliq":15.00,"irrf_f4_teto":4664.68,"irrf_f4_aliq":22.50,"fgts_aliquota":8.00,"hora_extra_aliq":50.00}'
               STOP RUN
           END-IF
           READ cf-file NEXT RECORD
               AT END DISPLAY '{"status":"erro"}' STOP RUN
           END-READ
           CLOSE cf-file
           MOVE cf-salario-minimo TO ws-je
           STRING '{"salario_minimo":' FUNCTION TRIM(ws-je)
               INTO ws-json-linha
           MOVE cf-inss-f1-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f1_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f1-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f1_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f2-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f2_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f2-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f2_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f3-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f3_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f3-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f3_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f4-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f4_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-inss-f4-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"inss_f4_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-ded-dep TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_ded_dep":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f1-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f1_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f1-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f1_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f2-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f2_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f2-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f2_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f3-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f3_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f3-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f3_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f4-teto TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f4_teto":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-irrf-f4-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"irrf_f4_aliq":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-fgts-aliquota TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"fgts_aliquota":' FUNCTION TRIM(ws-je) INTO ws-json-linha
           MOVE cf-hora-extra-aliq TO ws-je
           STRING FUNCTION TRIM(ws-json-linha)
               ',"hora_extra_aliq":' FUNCTION TRIM(ws-je) '}'
               INTO ws-json-linha
           DISPLAY FUNCTION TRIM(ws-json-linha).

       config-salvar.
           ACCEPT ws-valor-in FROM ENVIRONMENT "SALARIO_MINIMO"
           OPEN OUTPUT cf-file
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-salario-minimo
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F1_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f1-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F1_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f1-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F2_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f2-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F2_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f2-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F3_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f3-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F3_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f3-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F4_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f4-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS_F4_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-inss-f4-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_DED_DEP"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-ded-dep
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F1_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f1-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F1_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f1-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F2_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f2-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F2_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f2-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F3_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f3-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F3_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f3-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F4_TETO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f4-teto
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF_F4_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-irrf-f4-aliq
           ACCEPT ws-valor-in FROM ENVIRONMENT "FGTS_ALIQUOTA"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-fgts-aliquota
           ACCEPT ws-valor-in FROM ENVIRONMENT "HORA_EXTRA_ALIQ"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO cf-hora-extra-aliq
           WRITE cf-reg
           CLOSE cf-file
           DISPLAY "OK".

       holerite-gerar.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-data-in FROM ENVIRONMENT "COMPETENCIA"
           MOVE ws-data-in TO hl-competencia
           ACCEPT ws-valor-in FROM ENVIRONMENT "SALARIO_BASE"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-salario-base
           ACCEPT ws-horas-in FROM ENVIRONMENT "HORAS_EXTRAS"
           MOVE FUNCTION NUMVAL(ws-horas-in) TO hl-horas-extras
           ACCEPT ws-valor-in FROM ENVIRONMENT "VALOR_HORA_EXTRA"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-valor-hora-extra
           ACCEPT ws-valor-in FROM ENVIRONMENT "DSR"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-dsr
           ACCEPT ws-faltas-in FROM ENVIRONMENT "FALTAS"
           MOVE FUNCTION NUMVAL(ws-faltas-in) TO hl-faltas-dias
           ACCEPT ws-valor-in FROM ENVIRONMENT "PROVENTOS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-proventos
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-inss
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-irrf
           ACCEPT ws-valor-in FROM ENVIRONMENT "FGTS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-fgts
           ACCEPT ws-valor-in FROM ENVIRONMENT "OUTROS_DESC"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-outros-desc
           ACCEPT ws-valor-in FROM ENVIRONMENT "TOTAL_DESC"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-total-desc
           ACCEPT ws-valor-in FROM ENVIRONMENT "LIQUIDO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO hl-liquido

           IF ws-func-id = 0 THEN
               DISPLAY "ERRO: funcionario obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT hl-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT hl-file CLOSE hl-file
               OPEN INPUT hl-file END-IF
           PERFORM UNTIL 1 = 2
               READ hl-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF hl-id > ws-prox-id THEN MOVE hl-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE hl-file
           ADD 1 TO ws-prox-id

           ACCEPT hl-nome FROM ENVIRONMENT "NOME"
           OPEN EXTEND hl-file
           MOVE ws-prox-id TO hl-id
           MOVE ws-func-id TO hl-func-id
           MOVE "C" TO hl-situacao
           MOVE SPACES TO hl-data-pagamento
           WRITE hl-reg
           CLOSE hl-file
           MOVE ws-prox-id TO ws-id-ed
           DISPLAY FUNCTION TRIM(ws-id-ed).

       holerite-listar.
           OPEN INPUT hl-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"holerites":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"holerites":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ hl-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE hl-id TO ws-id-ed
               MOVE hl-func-id TO ws-func-id-ed
               MOVE hl-salario-base TO ws-je
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                   ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                   ',"nome":"' FUNCTION TRIM(hl-nome) '"'
                   ',"competencia":"' FUNCTION TRIM(hl-competencia) '"'
                   ',"salario_base":' FUNCTION TRIM(ws-je)
                   INTO ws-json-linha
               MOVE hl-horas-extras TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"horas_extras":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-valor-hora-extra TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"valor_hora_extra":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-dsr TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"dsr":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-faltas-dias TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"faltas":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-proventos TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"proventos":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-inss TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"inss":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-irrf TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"irrf":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-fgts TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"fgts":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-outros-desc TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"outros_descontos":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-total-desc TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"total_descontos":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE hl-liquido TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"liquido":' FUNCTION TRIM(ws-je)
                   ',"situacao":"' hl-situacao '"'
                   ',"data_pagamento":"' FUNCTION TRIM(hl-data-pagamento) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE hl-file.

       holerite-pagar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_PAGAMENTO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT hl-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ hl-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF hl-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "P" TO hl-situacao
                   MOVE ws-data-in TO hl-data-pagamento
               END-IF
               MOVE hl-id TO tl-id
               MOVE hl-func-id TO tl-func-id
               MOVE hl-nome TO tl-nome
               MOVE hl-competencia TO tl-competencia
               MOVE hl-salario-base TO tl-salario-base
               MOVE hl-horas-extras TO tl-horas-extras
               MOVE hl-valor-hora-extra TO tl-valor-hora-extra
               MOVE hl-dsr TO tl-dsr
               MOVE hl-faltas-dias TO tl-faltas-dias
               MOVE hl-proventos TO tl-proventos
               MOVE hl-inss TO tl-inss
               MOVE hl-irrf TO tl-irrf
               MOVE hl-fgts TO tl-fgts
               MOVE hl-outros-desc TO tl-outros-desc
               MOVE hl-total-desc TO tl-total-desc
               MOVE hl-liquido TO tl-liquido
               MOVE hl-situacao TO tl-situacao
               MOVE hl-data-pagamento TO tl-data-pagamento
               WRITE temp-reg
           END-PERFORM
           CLOSE hl-file CLOSE temp-file
           CALL "system" USING "mv dados/holerites.tmp dados/holerites.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       holerite-excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT hl-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT temp-file
           PERFORM UNTIL 1 = 2
               READ hl-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF hl-id NOT = ws-id THEN
                   MOVE hl-id TO tl-id
                   MOVE hl-func-id TO tl-func-id
                   MOVE hl-nome TO tl-nome
                   MOVE hl-competencia TO tl-competencia
                   MOVE hl-salario-base TO tl-salario-base
                   MOVE hl-horas-extras TO tl-horas-extras
                   MOVE hl-valor-hora-extra TO tl-valor-hora-extra
                   MOVE hl-dsr TO tl-dsr
                   MOVE hl-faltas-dias TO tl-faltas-dias
                   MOVE hl-proventos TO tl-proventos
                   MOVE hl-inss TO tl-inss
                   MOVE hl-irrf TO tl-irrf
                   MOVE hl-fgts TO hl-fgts
                   MOVE hl-outros-desc TO tl-outros-desc
                   MOVE hl-total-desc TO tl-total-desc
                   MOVE hl-liquido TO tl-liquido
                   MOVE hl-situacao TO tl-situacao
                   MOVE hl-data-pagamento TO tl-data-pagamento
                   WRITE temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE hl-file CLOSE temp-file
           CALL "system" USING "mv dados/holerites.tmp dados/holerites.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       ferias-incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-nome-in FROM ENVIRONMENT "NOME"
           ACCEPT ws-data-in FROM ENVIRONMENT "AQUIS_INICIO"
           MOVE ws-data-in TO fe-aquis-inicio
           ACCEPT ws-data-in FROM ENVIRONMENT "AQUIS_FIM"
           MOVE ws-data-in TO fe-aquis-fim
           ACCEPT ws-data-in FROM ENVIRONMENT "INICIO"
           MOVE ws-data-in TO fe-inicio
           ACCEPT ws-data-in FROM ENVIRONMENT "FIM"
           MOVE ws-data-in TO fe-fim
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS"
           MOVE FUNCTION NUMVAL(ws-dias-in) TO fe-dias
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS_ABONO"
           MOVE FUNCTION NUMVAL(ws-dias-in) TO fe-dias-abono
           ACCEPT ws-valor-in FROM ENVIRONMENT "VALOR_BASE"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-valor-base
           ACCEPT ws-valor-in FROM ENVIRONMENT "1_3"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-1-3
           ACCEPT ws-valor-in FROM ENVIRONMENT "ABONO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-abono
           ACCEPT ws-valor-in FROM ENVIRONMENT "ABONO_1_3"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-abono-1-3
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-inss
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-irrf
           ACCEPT ws-valor-in FROM ENVIRONMENT "LIQUIDO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO fe-liquido

           IF ws-func-id = 0 THEN
               DISPLAY "ERRO: funcionario obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT fe-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT fe-file CLOSE fe-file
               OPEN INPUT fe-file END-IF
           PERFORM UNTIL 1 = 2
               READ fe-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fe-id > ws-prox-id THEN MOVE fe-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE fe-file
           ADD 1 TO ws-prox-id

           MOVE ws-nome-in TO fe-nome
           OPEN EXTEND fe-file
           MOVE ws-prox-id TO fe-id
           MOVE ws-func-id TO fe-funcionario-id
           MOVE "C" TO fe-situacao
           MOVE SPACES TO fe-data-pagamento
           WRITE fe-reg
           CLOSE fe-file
           MOVE ws-prox-id TO ws-id-ed
           DISPLAY FUNCTION TRIM(ws-id-ed).

       ferias-listar.
           OPEN INPUT fe-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"ferias":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"ferias":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ fe-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE fe-id TO ws-id-ed
               MOVE fe-funcionario-id TO ws-func-id-ed
               MOVE fe-valor-base TO ws-je
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                   ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                   ',"nome":"' FUNCTION TRIM(fe-nome) '"'
                   ',"aquis_inicio":"' FUNCTION TRIM(fe-aquis-inicio) '"'
                   ',"aquis_fim":"' FUNCTION TRIM(fe-aquis-fim) '"'
                   ',"inicio":"' FUNCTION TRIM(fe-inicio) '"'
                   ',"fim":"' FUNCTION TRIM(fe-fim) '"'
                   ',"dias":' FUNCTION TRIM(ws-je)
                   INTO ws-json-linha
               MOVE fe-dias-abono TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"dias_abono":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-valor-base TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"valor_base":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-1-3 TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"1_3":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-abono TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"abono":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-abono-1-3 TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"abono_1_3":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-inss TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"inss":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-irrf TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"irrf":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE fe-liquido TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"liquido":' FUNCTION TRIM(ws-je)
                   ',"situacao":"' fe-situacao '"'
                   ',"data_pagamento":"' FUNCTION TRIM(fe-data-pagamento) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE fe-file.

       ferias-pagar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_PAGAMENTO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT fe-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT fe-temp
           PERFORM UNTIL 1 = 2
               READ fe-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fe-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "P" TO fe-situacao
                   MOVE ws-data-in TO fe-data-pagamento
               END-IF
               MOVE fe-id TO te-id
               MOVE fe-funcionario-id TO te-funcionario-id
               MOVE fe-nome TO te-nome
               MOVE fe-aquis-inicio TO te-aquis-inicio
               MOVE fe-aquis-fim TO te-aquis-fim
               MOVE fe-inicio TO te-inicio
               MOVE fe-fim TO te-fim
               MOVE fe-dias TO te-dias
               MOVE fe-dias-abono TO te-dias-abono
               MOVE fe-valor-base TO te-valor-base
               MOVE fe-1-3 TO te-1-3
               MOVE fe-abono TO te-abono
               MOVE fe-abono-1-3 TO te-abono-1-3
               MOVE fe-inss TO te-inss
               MOVE fe-irrf TO te-irrf
               MOVE fe-liquido TO te-liquido
               MOVE fe-situacao TO te-situacao
               MOVE fe-data-pagamento TO te-data-pagamento
               WRITE fe-temp-reg
           END-PERFORM
           CLOSE fe-file CLOSE fe-temp
           CALL "system" USING "mv dados/ferias.tmp dados/ferias.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       ferias-excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT fe-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT fe-temp
           PERFORM UNTIL 1 = 2
               READ fe-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF fe-id NOT = ws-id THEN
                   MOVE fe-id TO te-id
                   MOVE fe-funcionario-id TO te-funcionario-id
                   MOVE fe-nome TO te-nome
                   MOVE fe-aquis-inicio TO te-aquis-inicio
                   MOVE fe-aquis-fim TO te-aquis-fim
                   MOVE fe-inicio TO te-inicio
                   MOVE fe-fim TO te-fim
                   MOVE fe-dias TO te-dias
                   MOVE fe-dias-abono TO te-dias-abono
                   MOVE fe-valor-base TO te-valor-base
                   MOVE fe-1-3 TO te-1-3
                   MOVE fe-abono TO te-abono
                   MOVE fe-abono-1-3 TO te-abono-1-3
                   MOVE fe-inss TO te-inss
                   MOVE fe-irrf TO te-irrf
                   MOVE fe-liquido TO te-liquido
                   MOVE fe-situacao TO te-situacao
                   MOVE fe-data-pagamento TO te-data-pagamento
                   WRITE fe-temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE fe-file CLOSE fe-temp
           CALL "system" USING "mv dados/ferias.tmp dados/ferias.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       decimo-incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-nome-in FROM ENVIRONMENT "NOME"
           ACCEPT ws-ano-in FROM ENVIRONMENT "ANO"
           ACCEPT ws-parcela-in FROM ENVIRONMENT "PARCELA"
           ACCEPT ws-valor-in FROM ENVIRONMENT "VALOR_BASE"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO de-valor-base
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO de-inss
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO de-irrf
           ACCEPT ws-valor-in FROM ENVIRONMENT "LIQUIDO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO de-liquido

           IF ws-func-id = 0 THEN
               DISPLAY "ERRO: funcionario obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT de-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT de-file CLOSE de-file
               OPEN INPUT de-file END-IF
           PERFORM UNTIL 1 = 2
               READ de-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF de-id > ws-prox-id THEN MOVE de-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE de-file
           ADD 1 TO ws-prox-id

           MOVE ws-nome-in TO de-nome
           MOVE ws-ano-in TO de-ano
           MOVE ws-parcela-in TO de-parcela
           OPEN EXTEND de-file
           MOVE ws-prox-id TO de-id
           MOVE ws-func-id TO de-funcionario-id
           MOVE "C" TO de-situacao
           MOVE SPACES TO de-data-pagamento
           WRITE de-reg
           CLOSE de-file
           MOVE ws-prox-id TO ws-id-ed
           DISPLAY FUNCTION TRIM(ws-id-ed).

       decimo-listar.
           OPEN INPUT de-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"decimos":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"decimos":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ de-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE de-id TO ws-id-ed
               MOVE de-funcionario-id TO ws-func-id-ed
               MOVE de-valor-base TO ws-je
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                   ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                   ',"nome":"' FUNCTION TRIM(de-nome) '"'
                   ',"ano":"' FUNCTION TRIM(de-ano) '"'
                   ',"parcela":"' de-parcela '"'
                   ',"valor_base":' FUNCTION TRIM(ws-je)
                   INTO ws-json-linha
               MOVE de-inss TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"inss":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE de-irrf TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"irrf":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE de-liquido TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"liquido":' FUNCTION TRIM(ws-je)
                   ',"situacao":"' de-situacao '"'
                   ',"data_pagamento":"' FUNCTION TRIM(de-data-pagamento) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE de-file.

       decimo-pagar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_PAGAMENTO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT de-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT de-temp
           PERFORM UNTIL 1 = 2
               READ de-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF de-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "P" TO de-situacao
                   MOVE ws-data-in TO de-data-pagamento
               END-IF
               MOVE de-id TO qe-id
               MOVE de-funcionario-id TO qe-funcionario-id
               MOVE de-nome TO qe-nome
               MOVE de-ano TO qe-ano
               MOVE de-parcela TO qe-parcela
               MOVE de-valor-base TO qe-valor-base
               MOVE de-inss TO qe-inss
               MOVE de-irrf TO qe-irrf
               MOVE de-liquido TO qe-liquido
               MOVE de-situacao TO qe-situacao
               MOVE de-data-pagamento TO qe-data-pagamento
               WRITE de-temp-reg
           END-PERFORM
           CLOSE de-file CLOSE de-temp
           CALL "system" USING "mv dados/decimo.tmp dados/decimo.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       decimo-excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT de-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT de-temp
           PERFORM UNTIL 1 = 2
               READ de-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF de-id NOT = ws-id THEN
                   MOVE de-id TO qe-id
                   MOVE de-funcionario-id TO qe-funcionario-id
                   MOVE de-nome TO qe-nome
                   MOVE de-ano TO qe-ano
                   MOVE de-parcela TO qe-parcela
                   MOVE de-valor-base TO qe-valor-base
                   MOVE de-inss TO qe-inss
                   MOVE de-irrf TO qe-irrf
                   MOVE de-liquido TO qe-liquido
                   MOVE de-situacao TO qe-situacao
                   MOVE de-data-pagamento TO qe-data-pagamento
                   WRITE de-temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE de-file CLOSE de-temp
           CALL "system" USING "mv dados/decimo.tmp dados/decimo.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       rescisao-incluir.
           ACCEPT ws-func-id-in FROM ENVIRONMENT "FUNCIONARIO_ID"
           COMPUTE ws-func-id = FUNCTION NUMVAL(ws-func-id-in)
           ACCEPT ws-nome-in FROM ENVIRONMENT "NOME"
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_DESLIG"
           MOVE ws-data-in TO re-data-deslig
           ACCEPT ws-tipo-aviso-in FROM ENVIRONMENT "TIPO_AVISO"
           ACCEPT ws-dias-in FROM ENVIRONMENT "DIAS_AVISO"
           MOVE FUNCTION NUMVAL(ws-dias-in) TO re-dias-aviso
           ACCEPT ws-valor-in FROM ENVIRONMENT "SALDO_SALARIO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-saldo-salario
           ACCEPT ws-valor-in FROM ENVIRONMENT "FERIAS_VENC"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-ferias-venc
           ACCEPT ws-valor-in FROM ENVIRONMENT "FERIAS_PROP"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-ferias-prop
           ACCEPT ws-valor-in FROM ENVIRONMENT "1_3_FERIAS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-1-3-ferias
           ACCEPT ws-valor-in FROM ENVIRONMENT "13_PROP"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-13-prop
           ACCEPT ws-valor-in FROM ENVIRONMENT "FGTS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-fgts
           ACCEPT ws-valor-in FROM ENVIRONMENT "MULTA_FGTS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-multa-fgts
           ACCEPT ws-valor-in FROM ENVIRONMENT "INSS"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-inss
           ACCEPT ws-valor-in FROM ENVIRONMENT "IRRF"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-irrf
           ACCEPT ws-valor-in FROM ENVIRONMENT "LIQUIDO"
           MOVE FUNCTION NUMVAL(ws-valor-in) TO re-liquido

           IF ws-func-id = 0 THEN
               DISPLAY "ERRO: funcionario obrigatorio" STOP RUN END-IF

           MOVE 0 TO ws-prox-id
           OPEN INPUT re-file
           IF ws-file-status = "35" THEN
               OPEN OUTPUT re-file CLOSE re-file
               OPEN INPUT re-file END-IF
           PERFORM UNTIL 1 = 2
               READ re-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF re-id > ws-prox-id THEN MOVE re-id TO ws-prox-id END-IF
           END-PERFORM
           CLOSE re-file
           ADD 1 TO ws-prox-id

           MOVE ws-nome-in TO re-nome
           MOVE ws-tipo-aviso-in TO re-tipo-aviso
           OPEN EXTEND re-file
           MOVE ws-prox-id TO re-id
           MOVE ws-func-id TO re-funcionario-id
           MOVE "C" TO re-situacao
           MOVE SPACES TO re-data-pagamento
           WRITE re-reg
           CLOSE re-file
           MOVE ws-prox-id TO ws-id-ed
           DISPLAY FUNCTION TRIM(ws-id-ed).

       rescisao-listar.
           OPEN INPUT re-file
           IF ws-file-status = "35" THEN
               DISPLAY '{"rescisoes":[],"total":0}'
               STOP RUN END-IF
           DISPLAY '{"rescisoes":['
           MOVE "S" TO ws-encontrou
           MOVE 0 TO ws-total
           PERFORM UNTIL 1 = 2
               READ re-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               ADD 1 TO ws-total
               IF ws-encontrou = "S" THEN MOVE "N" TO ws-encontrou
               ELSE DISPLAY "," END-IF
               MOVE re-id TO ws-id-ed
               MOVE re-funcionario-id TO ws-func-id-ed
               MOVE re-saldo-salario TO ws-je
               STRING '{"id":' FUNCTION TRIM(ws-id-ed)
                   ',"funcionario_id":' FUNCTION TRIM(ws-func-id-ed)
                   ',"nome":"' FUNCTION TRIM(re-nome) '"'
                   ',"data_deslig":"' FUNCTION TRIM(re-data-deslig) '"'
                   ',"tipo_aviso":"' FUNCTION TRIM(re-tipo-aviso) '"'
                   ',"dias_aviso":' FUNCTION TRIM(ws-je)
                   INTO ws-json-linha
               MOVE re-saldo-salario TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"saldo_salario":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-ferias-venc TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"ferias_venc":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-ferias-prop TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"ferias_prop":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-1-3-ferias TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"1_3_ferias":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-13-prop TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"13_prop":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-fgts TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"fgts":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-multa-fgts TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"multa_fgts":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-inss TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"inss":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-irrf TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"irrf":' FUNCTION TRIM(ws-je) INTO ws-json-linha
               MOVE re-liquido TO ws-je
               STRING FUNCTION TRIM(ws-json-linha)
                   ',"liquido":' FUNCTION TRIM(ws-je)
                   ',"situacao":"' re-situacao '"'
                   ',"data_pagamento":"' FUNCTION TRIM(re-data-pagamento) '"}'
                   INTO ws-json-linha
               DISPLAY FUNCTION TRIM(ws-json-linha)
           END-PERFORM
           MOVE ws-total TO ws-total-ed
           DISPLAY '],"total":' FUNCTION TRIM(ws-total-ed) '}'
           CLOSE re-file.

       rescisao-pagar.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           ACCEPT ws-data-in FROM ENVIRONMENT "DATA_PAGAMENTO"
           MOVE "N" TO ws-encontrou
           OPEN INPUT re-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT re-temp
           PERFORM UNTIL 1 = 2
               READ re-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF re-id = ws-id THEN
                   MOVE "S" TO ws-encontrou
                   MOVE "P" TO re-situacao
                   MOVE ws-data-in TO re-data-pagamento
               END-IF
               MOVE re-id TO se-id
               MOVE re-funcionario-id TO se-funcionario-id
               MOVE re-nome TO se-nome
               MOVE re-data-deslig TO se-data-deslig
               MOVE re-tipo-aviso TO se-tipo-aviso
               MOVE re-dias-aviso TO se-dias-aviso
               MOVE re-saldo-salario TO se-saldo-salario
               MOVE re-ferias-venc TO se-ferias-venc
               MOVE re-ferias-prop TO se-ferias-prop
               MOVE re-1-3-ferias TO se-1-3-ferias
               MOVE re-13-prop TO se-13-prop
               MOVE re-fgts TO se-fgts
               MOVE re-multa-fgts TO se-multa-fgts
               MOVE re-inss TO se-inss
               MOVE re-irrf TO se-irrf
               MOVE re-liquido TO se-liquido
               MOVE re-situacao TO se-situacao
               MOVE re-data-pagamento TO se-data-pagamento
               WRITE re-temp-reg
           END-PERFORM
           CLOSE re-file CLOSE re-temp
           CALL "system" USING "mv dados/rescisoes.tmp dados/rescisoes.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

       rescisao-excluir.
           ACCEPT ws-id-in FROM ENVIRONMENT "ID"
           COMPUTE ws-id = FUNCTION NUMVAL(ws-id-in)
           MOVE "N" TO ws-encontrou
           OPEN INPUT re-file
           IF ws-file-status = "35" THEN
               DISPLAY "ERRO" STOP RUN END-IF
           OPEN OUTPUT re-temp
           PERFORM UNTIL 1 = 2
               READ re-file NEXT RECORD
                   AT END EXIT PERFORM
               END-READ
               IF re-id NOT = ws-id THEN
                   MOVE re-id TO se-id
                   MOVE re-funcionario-id TO se-funcionario-id
                   MOVE re-nome TO se-nome
                   MOVE re-data-deslig TO se-data-deslig
                   MOVE re-tipo-aviso TO se-tipo-aviso
                   MOVE re-dias-aviso TO se-dias-aviso
                   MOVE re-saldo-salario TO se-saldo-salario
                   MOVE re-ferias-venc TO se-ferias-venc
                   MOVE re-ferias-prop TO se-ferias-prop
                   MOVE re-1-3-ferias TO se-1-3-ferias
                   MOVE re-13-prop TO se-13-prop
                   MOVE re-fgts TO se-fgts
                   MOVE re-multa-fgts TO se-multa-fgts
                   MOVE re-inss TO se-inss
                   MOVE re-irrf TO se-irrf
                   MOVE re-liquido TO se-liquido
                   MOVE re-situacao TO se-situacao
                   MOVE re-data-pagamento TO se-data-pagamento
                   WRITE re-temp-reg
               ELSE MOVE "S" TO ws-encontrou
               END-IF
           END-PERFORM
           CLOSE re-file CLOSE re-temp
           CALL "system" USING "mv dados/rescisoes.tmp dados/rescisoes.dat"
           END-CALL
           IF ws-encontrou = "S" THEN DISPLAY "OK"
           ELSE DISPLAY "ERRO".

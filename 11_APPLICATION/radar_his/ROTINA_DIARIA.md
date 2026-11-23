# Rotina diária do Faro — roteiro do orquestrador

Disparada todo dia às 7h38 (horário de São Paulo), para o e-mail chegar por volta das 8h. Quem executa é o orquestrador (Claude), seguindo estes passos na ordem. Não pule o Auditor.

| Agente | O que faz | Onde |
|---|---|---|
| Coletor | Baixa alvarás HIS/HMP (GeoSampa), guias de ITBI (Fazenda), IPCA e CDI (Banco Central) | `coletar.py` |
| Analista | Liga alvarás às vendas, separa 1ª venda, revenda, lote e permuta, marca venda acima do teto | `processar.py` |
| Auditor | Confere quantidades e datas contra o dia anterior; pode **bloquear** | `auditor.py` |
| Redator | Escreve "O que mapeamos ontem" comparando com o snapshot anterior | `redator.py` |
| Distribuidor | Publica o site no mesmo link e envia o e-mail | este roteiro (passos 5 e 6) |
| Orquestrador | Roda tudo, decide publicar ou não, registra e avisa | este roteiro |

## Passos

1. **Atualizar o código.** No repositório (`/home/user/beco_teste` ou o diretório de trabalho atual):
   `git fetch origin claude/beco-real-estate-intelligence-i322uf && git merge --ff-only FETCH_HEAD`
2. **Dependências.** `pip install -q -r 11_APPLICATION/radar_his/requirements.txt`
3. **Rodar os agentes.** `cd 11_APPLICATION/radar_his && python3 rotina_diaria.py`
   Leva de 3 a 5 minutos (baixa cerca de 550 MB de ITBI quando a máquina é nova). Código de saída 2 = Auditor bloqueou.
4. **Ler `saida/boletim.json`.** Se `status` for `bloqueado`: **não publicar nem enviar**. Avise na conversa quais verificações falharam (`auditoria.verificacoes` com `ok: false`) e pare.
5. **Publicar o site.** Ferramenta Artifact, `publish`, com:
   - `file_path` = `site.file_path`; `root` = `site.root`; `files` = `[{"path": p} for p in site.files]`
   - sem `capabilities` (mantém as que a página já tem); sem `icon`.
   - Se a publicação for recusada porque esta conversa não leu o artefato, faça `read` de `site.url` e publique de novo passando `url` = `site.url`.
6. **Enviar o e-mail.**
   - Se `destinatarios` tiver endereços: `mcp__Gmail__send_message` com `to` = `destinatarios`, `cc` = `copia`, `subject` = `assunto`, `htmlBody` = `html`, `body` = `texto` (sem anexos: o logo é desenhado no próprio HTML).
   - Se `destinatarios` estiver vazio: `mcp__Gmail__create_draft` com os mesmos campos (sem `to`) e avise que falta o e-mail do Diogo em `config.json`.
7. **Registrar.** `git add 11_APPLICATION/radar_his/estado 11_APPLICATION/radar_his/boletins`, commit `Faro: boletim AAAA-MM-DD` (com as linhas de atribuição da sessão) e `git push origin claude/beco-real-estate-intelligence-i322uf`.
8. **Responder** em até 3 linhas: status do Auditor, assunto do e-mail, e se foi enviado ou ficou como rascunho.

## Configuração

`config.json`:
- `destinatarios`: e-mails que recebem o boletim (ex.: o do Diogo).
- `copia`: cópias.
- `link_radar`: link do site; os botões do e-mail abrem a ficha do imóvel (`#imovel-<id>`).

Quem recebe o e-mail precisa ter acesso ao link do site (menu Share da página) para os botões abrirem.

## Registros

- `estado/snapshot.json`: o que já foi mapeado; base de comparação do dia seguinte.
- `estado/execucoes.jsonl`: uma linha por execução, com a duração de cada agente, o status e as falhas.
- `boletins/AAAA-MM-DD.html`: cópia de cada boletim enviado.

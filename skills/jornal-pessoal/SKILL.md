---
name: jornal-pessoal
description: Monta um jornal diário personalizado em PDF (estilo broadsheet clássico, A4, até 2 páginas, preto e branco para imprimir) para qualquer pessoa. Usa a memória do Claude sobre o leitor (cidade, profissão, times, hobbies, interesses) para escolher as pautas, apura as notícias do dia na web com fonte em cada nota, inclui o tempo local, a agenda do dia se o calendário estiver conectado, salva o PDF e, no final, sempre manda para a impressora do computador do leitor. Use SEMPRE que o usuário pedir "meu jornal", "jornal do dia", "jornal personalizado", "edição de hoje", "newspaper", "daily paper", "um resumo de notícias para imprimir", "briefing em PDF estilo jornal", ou quiser montar/agendar uma edição diária com as notícias que importam para ele, mesmo sem dizer "skill" ou "PDF".
---

# Jornal pessoal

Produz a edição de hoje de um jornal feito para um único leitor: o usuário. O valor está em três coisas, nesta ordem: **as pautas certas para essa pessoa**, **fatos verificados e recentes**, e **um PDF bonito que cabe em 2 páginas**. Se faltar uma delas, o jornal vira só mais um resumo genérico.

## 1. Conhecer o leitor (antes de qualquer busca)

O jornal só fica pessoal se as pautas vierem de quem lê. Monte um perfil curto:

1. **Memória do Claude.** Se existirem ferramentas de memória (`memory_list` / `memory_read`, ou um bloco `<user_memory>` / perfil já no contexto), leia o perfil, as preferências e os arquivos de tópicos e áreas que tratam de interesses, trabalho, cidade e hobbies. Extraia:
   - nome ou apelido (para o título do jornal), idioma preferido, cidade e fuso horário;
   - profissão e setor (vira uma pauta de mercado: concorrentes, tendências do setor);
   - times, esportes, jogos e esports que acompanha;
   - tecnologias, hobbies e projetos (ex.: IA, impressão 3D, corrida, culinária);
   - preferências de formato que a pessoa já declarou.
2. **Pedido atual e instruções de tarefa agendada.** Se o prompt já lista pautas, cidade ou nome, isso vence a memória.
3. **Sem memória suficiente:**
   - com alguém respondendo, faça **uma** pergunta curta (cidade + 3 interesses + nome do jornal);
   - em execução agendada ou sem resposta, use o que tiver (e-mail e organização do usuário dão pistas de idioma e setor), complete com pautas gerais (tecnologia, economia, ciência, cidade) e diga a suposição no resumo final.

**Privacidade, porque papel impresso circula:** nunca coloque no jornal dados sensíveis vindos da memória (saúde, finanças pessoais, família, religião, política pessoal etc.). Use a memória só para *escolher* pautas, não para *publicar* fatos sobre o leitor. A agenda entra só com título e horário.

## 2. Definir as pautas da edição

- **Fixas (todo dia):** as 2–4 paixões mais fortes do leitor (ex.: o time de coração, a área profissional, um esport) + **página local** da cidade (tempo, notícias da prefeitura/governo, trânsito, 1–3 eventos culturais).
- **Dinâmicas (2–4 por dia):** escolha entre os interesses secundários e o que for notícia boa hoje (economia rápida, ciência, gadgets, setor da empresa etc.). Varie de um dia para o outro.
- **Manchete:** a notícia de maior impacto *para esse leitor* hoje: o jogo decisivo do time dele, um grande lançamento na área dele, um fato marcante na cidade. Não precisa ser a maior notícia do mundo.

## 3. Apuração

Dispare as buscas em paralelo (WebSearch; WebFetch nas páginas mais promissoras). Regras que mantêm o jornal confiável:

- Só entram fatos publicados nas **últimas 24–48 h** e confirmados na página da fonte. Leia a data da matéria: buscas devolvem muito conteúdo velho com cara de novo.
- **Nunca invente** placar, horário, adversário, número ou declaração. Se não achou, omita ou escreva "sem jogos confirmados hoje". Uma lacuna honesta vale mais que um dado bonito e errado.
- Quando duas fontes divergem (ex.: placar de um mapa), publique só a parte em que concordam.
- Para jogos e eventos, converta todos os horários para o fuso do leitor e diga o fuso uma vez.
- Escreva com suas palavras, sem copiar parágrafos, e termine cada nota com a fonte curta entre parênteses: "(HLTV)", "(G1)", "(Reuters)".
- **Tempo:** máx./mín., chuva (% e mm), umidade e alerta (seca, calor, temporal) quando houver. Confira se a página traz a previsão *de hoje*, e não a de ontem que ficou em cache.
- **Agenda (opcional):** se houver ferramenta de calendário (ex.: Google Calendar `list_events`), liste os compromissos de hoje no fuso do leitor, só com horário e título. Se cruzar com algo do jornal (jogo no meio de uma reunião), vale uma nota curta e simpática. Sem calendário, não inclua o box.

## 4. Diagramação

Use o template e o script da skill. Eles já resolvem fontes, hifenização e conferência de tamanho.

1. Copie `assets/template.html` para uma pasta de trabalho como `index.html` e preencha os campos `{{ }}`. Apague blocos não usados e duplique os blocos `.story` à vontade.
2. **Nameplate:** padrão "The [Nome] Chronicle" (ou o nome que o leitor escolheu), em fonte gótica. Crie um lema curto próprio. **Não** use nome, logo ou slogan de jornal real: o leitor vai imprimir e mostrar para outras pessoas, e imitar marca real é cópia.
3. **Faixa de data:** "[Cidade], [dia da semana], [data por extenso]" · lema · "Edição nº N". Para N, conte as edições anteriores na pasta de destino (`*-AAAA-MM-DD.pdf`) + 1, ou use a regra que a tarefa agendada definir.
4. **Página 1:** ear com o tempo (esquerda) e ear com o destaque do dia (direita); manchete em 2 colunas com capitular, linha fina e crédito "Por [nome do jornal]"; duas colunas laterais com as pautas fixas mais fortes (uma delas em lista de notas curtas).
5. **Página 2:** página local (cidade + agenda cultural em tabela), pautas dinâmicas, agenda do leitor (se houver) e o rodapé "Fontes" com as URLs principais em letra miúda (sem `https://`, encurtadas).
6. Só preto e cinza, sem imagens externas. Use filetes, boxes, tabelas para placares e agenda, e ornamentos ❧ ✦ ■.
7. Escreva no idioma do leitor e ajuste `lang` no `<html>`.

### Renderizar e conferir

```bash
pip install playwright pyphen beautifulsoup4 --break-system-packages   # se faltar
python3 <skill>/scripts/render.py <pasta_trabalho> <saida.pdf> --lang pt-BR --png
```

O script imprime, para cada coluna, quantos pixels sobram (negativo) ou vazam (positivo), além do número de páginas e das prévias PNG em `<pasta>/build/`. Como `.page` esconde o que vaza, **o texto excedente some sem aviso no PDF**. Por isso:

- Se alguma coluna der positivo ou houver mais de 2 páginas: corte primeiro as notas menos importantes, depois encurte parágrafos, mova notas entre colunas que têm sobra e, por último, reduza levemente o corpo (`body{font-size}`), nunca abaixo de 8,5 pt.
- Abra `preview-1.png` com a ferramenta de leitura de imagem e **olhe**: título da manchete muito alto, coluna vazia demais, ear encostando no nameplate, tabela estourando. Rode de novo até ficar limpo. Sobras grandes (−150 px ou mais) numa coluna pedem mais uma nota curta ali.
- Se o Chromium não estiver no ambiente, `playwright install chromium` resolve. Se a rede bloquear, use o Chromium do sistema via `executable_path`.

## 5. Entrega

1. Nome do arquivo: `<slug-do-jornal>-AAAA-MM-DD.pdf` (data de hoje no fuso do leitor).
2. Salve na pasta de saídas da sessão e envie o arquivo ao usuário (SendUserFile ou equivalente).
3. Se houver uma pasta do computador do usuário conectada, ou o pedido citar uma, grave o PDF lá também. Se não der para gravar, avise em uma frase e deixe o anexo.
4. **Mande para a impressora. Este é sempre o último passo.** O jornal foi feito para ser lido no papel, então a edição só termina quando é impressa. Veja "Impressão" abaixo.
5. Feche com 2–3 linhas no idioma do leitor: a manchete, o compromisso de horário mais importante do dia (jogo, evento), onde o arquivo ficou e se foi impresso (em qual impressora).
6. Em execução agendada, mande essas mesmas linhas como notificação, se a ferramenta existir. É assim que o leitor fica sabendo que a edição saiu. Se a impressão falhar, diga isso logo na primeira frase, porque é o que ele precisa resolver.

### Impressão

A impressora está no computador do leitor, não no ambiente na nuvem. Então o PDF precisa estar **gravado numa pasta do computador** (passo 3) antes de imprimir, e o comando roda **no sistema do computador**. No macOS isso é a ferramenta de AppleScript (ex.: `Control_your_Mac__osascript`) com `do shell script`. O shell Linux da sessão (`device_bash`) não enxerga a impressora.

1. **Descubra a impressora:** `lpstat -p -d`.
   - Se o leitor ou a tarefa agendada indicou uma impressora, use essa.
   - Senão, use a padrão do sistema.
   - Sem padrão, mas com uma impressora só, use essa.
   - Com várias e nenhuma escolhida: se alguém estiver respondendo, pergunte uma vez. Se não, use a primeira habilitada e diga qual foi.
2. **Imprima em A4 e em cinza.** Muitas impressoras vêm com Carta/Letter como padrão e cortariam o rodapé. O jornal é preto e branco, então o modo cinza economiza tinta colorida:

   ```applescript
   do shell script "lp -d 'NOME_DA_IMPRESSORA' -o media=A4 -o fit-to-page -o ColorModel=Gray -t 'Jornal AAAA-MM-DD' '/caminho/no/computador/arquivo.pdf'"
   ```

   Se a impressora recusar alguma opção (`ColorModel` varia de modelo para modelo; confira com `lpoptions -p NOME -l`), tire só essa opção e tente de novo.
3. **Confira** com `lpstat -o` (fila) ou pela linha `request id is ...` que o `lp` devolve. Inclua esse id no resumo.
4. **Se não der para imprimir** (computador offline, nenhuma impressora, erro no `lp`): não tente outros caminhos. Deixe o PDF salvo e anexado, e diga no resumo que a impressão não saiu e por quê.
5. Uma edição, uma impressão. Se precisar renderizar de novo depois de já ter impresso, não reimprima sem pedido do leitor.

## Checklist rápido antes de entregar

- [ ] Pautas vieram do perfil do leitor, e nada sensível da memória foi publicado
- [ ] Toda nota tem fonte, e todo fato é de 24–48 h
- [ ] Horários no fuso do leitor
- [ ] `render.py` sem colunas positivas e com ≤ 2 páginas
- [ ] Prévia da página 1 conferida visualmente
- [ ] PDF entregue (e gravado na pasta do usuário, se houver)
- [ ] Enviado para a impressora em A4 (ou, se não deu, o motivo está no resumo)

# skills

Skills para o Claude e outros agentes compatíveis com o formato [Agent Skills](https://skills.sh).

## Instalação

```bash
npx skills add raphaelcunha/skills
```

Para instalar só uma skill:

```bash
npx skills add raphaelcunha/skills --skill cafe-e-tdah
```

## Skills

### `cafe-e-tdah` — Café & TDAH

Um jornal diário feito só para você. Sai em PDF A4, com até 2 páginas, em preto e branco, no estilo de um jornal impresso clássico, e pode ir direto para a impressora.

- **Setup rápido:** na primeira vez, a skill faz cerca de 5 perguntas, todas com uma resposta padrão:
  1. De onde vem o seu perfil? Pode ser a memória do Claude, a memória do Codex/ChatGPT ou de outra LLM (você cola o que ela sabe sobre você) ou respostas na hora.
  2. Quais são seus interesses e sua cidade?
  3. Qual o nome e o idioma do jornal? O padrão é "Café & TDAH".
  4. Onde salvar o PDF, e se deve imprimir no final, em qual impressora.
  5. Quer uma rotina diária? Pode ser uma tarefa agendada do app, cron/launchd no seu computador ou só sob demanda.

  As respostas ficam em `cafe-e-tdah.json`. Assim a rotina funciona com qualquer agente.
- **Apuração:** só notícias das últimas 24–48 h, com a fonte em cada nota. Se a skill não achar um dado, diz que não achou em vez de inventar.
- **O que a edição traz:** tempo local, página da cidade com agenda cultural e, se o calendário estiver conectado, os compromissos do dia.
- **Layout:** template HTML com fontes livres embutidas e o script `scripts/render.py`. O script hifeniza o texto, gera o PDF com Playwright/Chromium e avisa se alguma coluna estourou ou se passou de 2 páginas.
- **Impressão (opcional):** usa o `lp` do seu computador (macOS/Linux), em A4 e em tons de cinza.

Exemplos de pedido:

> "configura meu Café & TDAH"
> "monta meu jornal de hoje"

**Requisitos:** Python 3, `playwright` (com Chromium), `pyphen`, `beautifulsoup4` e `pdfinfo`/`pdftoppm` (poppler). Para imprimir, o agente precisa conseguir rodar comandos no computador onde a impressora está instalada.

## Licença

Código e instruções sob a licença MIT (veja `LICENSE`).

As fontes em `skills/cafe-e-tdah/assets/fonts/` são distribuídas sob a [SIL Open Font License 1.1](skills/cafe-e-tdah/assets/fonts/OFL-LICENSE.txt):

- Libre Caslon Text, de Pablo Impallari
- Old Standard TT, de Alexey Kryukov
- UnifrakturMaguntia, de j. 'mach' wust

Os arquivos vêm dos pacotes [Fontsource](https://fontsource.org).

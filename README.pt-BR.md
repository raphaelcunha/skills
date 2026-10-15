# skills

[![skills.sh](https://skills.sh/b/raphaelcunha/skills)](https://skills.sh/raphaelcunha/skills)

[English](README.md) · **Português (Brasil)**

Skills para o Claude e outros agentes compatíveis com o formato [Agent Skills](https://skills.sh).

## Instalação

```bash
npx skills add raphaelcunha/skills
```

Para instalar só uma skill:

```bash
npx skills add raphaelcunha/skills --skill coffee-and-adhd
```

## Skills

### `coffee-and-adhd` — Café & TDAH

Um jornal diário feito só para você. Sai como um PDF A4 de até 2 páginas, em preto e branco, com layout pensado para impressão (corpo serifado de 10 pt, um resumo de leitura rápida no topo e uma ilustração por edição), e pode ir direto para a sua impressora.

<p align="center">
  <img src="docs/sample-page-1.png" alt="Edição de exemplo do Café & TDAH, página 1" width="48%">
  <img src="docs/sample-page-2.png" alt="Edição de exemplo do Café & TDAH, página 2" width="48%">
</p>

<p align="center"><sub>Edição de exemplo para um leitor que só acompanha IA, feita com notícias reais publicadas entre 6 e 14 de outubro de 2026. Sem dados pessoais. <a href="docs/sample-edition.pdf">Baixe o PDF</a>.</sub></p>

- **Setup rápido:** na primeira vez, a skill faz umas 5 perguntas (mais uma sobre apps conectados), uma de cada vez, cada uma com uma resposta padrão que você pode só aceitar:
  1. Qual idioma? Sugere português do Brasil (PT-BR), inglês ou espanhol.
  2. De onde vem o seu perfil? Da memória do Claude, da memória do Codex/ChatGPT ou de outro LLM (você cola o que ele sabe sobre você), ou de respostas na hora.
  3. Seus interesses e sua cidade.
  4. O nome do jornal, que por padrão é "Café & TDAH" ("Coffee & ADHD" em inglês). E também: onde salvar o PDF, e se deve imprimir no final e em qual impressora.
  5. Se quer uma rotina diária: tarefa agendada no app, cron/launchd no seu computador, ou só quando você pedir.
  6. Quais apps conectados ela pode ler. Ela lista os conectores e plugins que encontrar (Gmail/Outlook, Slack/Teams, Google Agenda, Linear/Jira/GitHub, Granola/Fireflies, Notion/Drive) e sugere até 3 que ainda não estão conectados e ajudariam você.

  As respostas ficam salvas em `coffee-and-adhd.json`, então a rotina funciona com qualquer agente.
- **Apuração:** só notícias das últimas 24–48 horas, com fonte em cada item. Se a skill não encontra um dado, ela diz isso em vez de inventar.
- **O que vem numa edição:** o clima da sua cidade, uma página local com agenda cultural e, se você conectou apps, um quadro "Seu dia": reuniões de hoje, tarefas que vencem, PRs esperando sua revisão, to-dos das reuniões de ontem e quantos e-mails e menções chegaram. Newsletters do seu inbox também podem sugerir matérias, sempre citando a fonte pública.
- **Privacidade:** os apps conectados são só leitura (a skill nunca envia, responde ou marca nada como lido), e só horários, títulos, ids e contagens vão para o papel, nunca o texto das mensagens nem o nome de outras pessoas. E-mail e chat ficam desligados até você ligar.
- **Layout:** um template HTML com fontes abertas embutidas (Alfa Slab One, Rokkitt, Bitter), uma pequena biblioteca de ilustrações em preto e branco e o `scripts/render.py`. O script hifeniza o texto (pt-BR, en, es e outros), gera o PDF com Playwright/Chromium e avisa se alguma coluna estoura ou se o jornal passa de 2 páginas.
- **Impressão (opcional):** usa o `lp` no seu computador (macOS/Linux), em A4 e tons de cinza.

Exemplos de pedidos:

> "configura meu Café & TDAH"
> "monta meu jornal de hoje"
> "make today's edition of my newspaper"

**Requisitos:** Python 3, `playwright` (com Chromium), `pyphen`, `beautifulsoup4` e `pdfinfo`/`pdftoppm` (poppler). Para imprimir, o agente precisa conseguir rodar comandos no computador onde a impressora está ligada.

## Licença

O código e as instruções estão sob a licença MIT (veja `LICENSE`).

As fontes embutidas em `skills/coffee-and-adhd/assets/template.html` são distribuídas sob a [SIL Open Font License 1.1](skills/coffee-and-adhd/assets/FONTS-LICENSE.txt):

- Alfa Slab One, de JM Solé
- Rokkitt, de Vernon Adams
- Bitter, de Huerta Tipográfica

Os arquivos das fontes vêm dos pacotes do [Fontsource](https://fontsource.org).

# skills

Skills para o Claude e outros agentes compatíveis com o formato [Agent Skills](https://skills.sh).

## Instalação

```bash
npx skills add raphaelcunha/skills
```

Para instalar só uma skill:

```bash
npx skills add raphaelcunha/skills --skill jornal-pessoal
```

## Skills

### `jornal-pessoal`

Gera, todo dia, um jornal personalizado em PDF: A4, até 2 páginas, preto e branco, no estilo de um jornal impresso clássico. No final, manda o PDF para a impressora.

- **Pautas:** escolhidas a partir do que o agente sabe sobre o leitor, como cidade, profissão, times, hobbies e interesses. Se o agente tiver memória, a skill usa a memória. Se não tiver, faz uma única pergunta curta.
- **Apuração:** só notícias das últimas 24–48 h, com a fonte em cada nota. Se não achar um dado, diz que não achou em vez de inventar.
- **O que a edição traz:** tempo local, página da cidade com agenda cultural e, se o calendário estiver conectado, os compromissos do dia.
- **Layout:** template HTML com fontes livres embutidas e um script (`scripts/render.py`) que hifeniza o texto, gera o PDF com Playwright/Chromium e avisa se alguma coluna estourou ou se passou de 2 páginas.
- **Impressão:** usa o `lp` do computador do usuário (macOS/Linux), em A4 e em tons de cinza.

Exemplos de pedido:

> "monta meu jornal de hoje"
> "quero um jornal diário com as notícias do meu time, de IA e da minha cidade, para imprimir"

**Requisitos:** Python 3, `playwright` (com Chromium), `pyphen`, `beautifulsoup4` e `pdfinfo`/`pdftoppm` (poppler). Para imprimir, o agente precisa conseguir rodar comandos no computador onde a impressora está instalada.

## Licença

Código e instruções sob a licença MIT (veja `LICENSE`).

As fontes em `skills/jornal-pessoal/assets/fonts/` são distribuídas sob a [SIL Open Font License 1.1](skills/jornal-pessoal/assets/fonts/OFL-LICENSE.txt):

- Libre Caslon Text, de Pablo Impallari
- Old Standard TT, de Alexey Kryukov
- UnifrakturMaguntia, de j. 'mach' wust

Os arquivos vêm dos pacotes [Fontsource](https://fontsource.org).

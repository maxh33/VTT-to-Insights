# VTT-to-Insights

**Transforme transcrições de 3 horas de aula em resumos de estudo concisos em segundos.**

Chega de ler milhares de linhas de "ééé", "né" e ruídos de UUID. O VTT-to-Insights limpa arquivos `.vtt` brutos — removendo IDs de cue, mesclando fragmentos e eliminando repetições — para que você possa passar contexto limpo e otimizado em tokens para sua IA favorita (Claude, ChatGPT, Gemini) e obter resumos de estudo de alta qualidade.

---

## O Problema

Os portais universitários exportam gravações de aula como arquivos `.vtt`. Uma aula de 3 horas gera ~11.000 linhas:

```
bde3c4a1-7f2e-4b1a-9c3d-000000000042-0     ← UUID (lixo puro)
00:05:11.560 --> 00:05:16.738
O fundamento de IHC é a organização

bde3c4a1-7f2e-4b1a-9c3d-000000000043-0
00:05:16.738 --> 00:05:19.200
e arquitetura aplicada ao computador
```

Custo em tokens bruto: **~85k–100k tokens**. Muito barulhento para um resultado útil da IA.

Depois do VTT-to-Insights: **~55k–65k tokens**, parágrafos limpos com timestamps.

---

## Funcionalidades

- **Redução de Ruído** — Remove UUIDs, cabeçalhos WEBVTT, tags de tempo inline, linhas em branco
- **Otimização de Tokens** — Reduz o tamanho do arquivo em 30–40% para caber na janela de contexto da IA
- **Mesclagem Inteligente** — Converte cues fragmentadas em blocos de parágrafo legíveis de ~60 segundos
- **Preservação de Timestamps** — Cada bloco mantém seu marcador `[HH:MM:SS]` para navegar no vídeo
- **Biblioteca de Prompts** — Prompts prontos para anotações de estudo, resumos e extração de conceitos
- **Sem Dependências** — Python 3 puro, sem necessidade de `pip install`
- **Processamento em Lote** — Processe um semestre inteiro de VTTs com um loop shell

---

## Início Rápido

```bash
# Clone
git clone https://github.com/yourusername/VTT-to-Insights.git
cd VTT-to-Insights

# Execute (sem dependências)
python3 vtt_clean.py "Minha Aula 2024-02-04.vtt"
# → Minha Aula 2024-02-04_clean.txt

# Cole o _clean.txt no Claude.ai / ChatGPT com um prompt da pasta prompts/
```

---

## Formato de Saída

```
[00:03:10] A partir de hoje a gente vai começar um pouco teórico,
como construir ali um conhecimento para depois desse conhecimento,
tendo aquela base estruturada, a gente consiga fazer colocar em
prática ali. A gente vai mexer com Figma...

[00:05:11] O fundamento de IHC é a organização e arquitetura
aplicada ao computador humano. Interação humano computador...
```

---

## Biblioteca de Prompts

| Prompt | Quando Usar | Tempo de Leitura |
|--------|-------------|------------------|
| [`study-notes.md`](prompts/study-notes.md) | Análise acadêmica completa (5 seções) | ~5 min |
| [`quick-summary.md`](prompts/quick-summary.md) | Visão geral em 5 pontos | ~1 min |
| [`concepts-only.md`](prompts/concepts-only.md) | Glossário / terminologia | ~3 min |

Veja [`examples/sample_output.md`](examples/sample_output.md) para um exemplo real de saída.

---

## Fluxo de Trabalho

```
1. Baixe o .vtt do portal da faculdade          (~30 seg)
2. python3 vtt_clean.py "aula.vtt"             (~5 seg)
3. Abra Claude.ai / ChatGPT → Novo chat         (~10 seg)
4. Cole o prompt + conteúdo do _clean.txt       (~1 min)
5. Leia a análise e pule para os timestamps     (hora de estudar)
```

---

## Opções

```
python3 vtt_clean.py --help

argumentos posicionais:
  vtt_file              Caminho para o arquivo .vtt

opções:
  --block-seconds N     Segundos por bloco de parágrafo (padrão: 60)
  --output ARQUIVO, -o  Caminho personalizado para o arquivo de saída
  --stdout              Imprime na saída padrão (útil para pipes)
```

**Exemplos:**
```bash
# Blocos maiores (menos fragmentados)
python3 vtt_clean.py aula.vtt --block-seconds 90

# Copiar direto para a área de transferência (Linux)
python3 vtt_clean.py aula.vtt --stdout | xclip -selection clipboard

# Processar uma pasta inteira de VTTs
for f in aulas/*.vtt; do python3 vtt_clean.py "$f"; done
```

---

## Compatibilidade

Testado com arquivos VTT exportados de:
- **Microsoft Teams** (portais universitários)
- **Zoom** (legendas geradas automaticamente)
- **Google Meet** (com gravação de legendas)
- **YouTube** (auto-geradas, baixe com `yt-dlp --write-auto-sub`)

---

## Estrutura do Projeto

```
VTT-to-Insights/
├── vtt_clean.py               ← Script principal (sem dependências)
├── prompts/
│   ├── study-notes.md         ← Prompt de análise acadêmica completa (Português)
│   ├── quick-summary.md       ← Prompt de resumo rápido em 5 pontos
│   └── concepts-only.md       ← Prompt de extração de conceitos / glossário
├── examples/
│   └── sample_output.md       ← Exemplo de saída anonimizado
├── README.md                  ← Documentação em Inglês
├── README.pt-BR.md            ← Este arquivo
└── LICENSE                    ← MIT
```

---

## Contribuindo

Contribuições são bem-vindas! Especialmente:
- Suporte a outros dialetos VTT
- Diarização de falantes (separar quem fala)
- Mais templates de prompt (preparação para prova, geração de mapas mentais)
- Suporte a outros idiomas

Abra uma issue ou envie um PR.

---

## Licença

MIT — veja [LICENSE](LICENSE)

---

*Este projeto nasceu numa sala de aula de Ciência da Computação no Brasil 🇧🇷 para ajudar estudantes do mundo todo a lidar com transcrições longas de aula. Contribuições são bem-vindas!*

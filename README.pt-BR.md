# VTT-to-Insights

**Transforme transcrições de 3 horas de aula em resumos de estudo concisos em segundos.**

Chega de ler milhares de linhas de "ééé", "né" e ruídos de UUID. O VTT-to-Insights limpa arquivos `.vtt` brutos — removendo IDs de cue, mesclando fragmentos e eliminando repetições — para que você possa passar contexto limpo e otimizado em tokens para sua IA favorita (Claude, ChatGPT, Gemini) e obter resumos de estudo de alta qualidade.

> [Read in English](README.md)

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

Custo em tokens bruto: **~85k–100k tokens**. Muito barulhento para a IA produzir um resultado útil.

Depois do VTT-to-Insights: **~32k tokens**, parágrafos limpos com timestamps.

---

## Funcionalidades

- **Redução de Ruído** — Remove UUIDs, cabeçalhos WEBVTT, tags de tempo inline, linhas em branco
- **Otimização de Tokens** — Reduz o tamanho do arquivo em 60–70% para caber na janela de contexto da IA
- **Mesclagem Inteligente** — Converte cues fragmentadas em blocos de parágrafo legíveis de ~60 segundos
- **Preservação de Timestamps** — Cada bloco mantém seu marcador `[HH:MM:SS]` para navegar no vídeo
- **Biblioteca de Prompts Bilíngue** — Prompts prontos em Português e Inglês
- **Sem Dependências** — Python 3 puro, sem necessidade de `pip install`
- **Multiplataforma** — Funciona no Windows, Mac e Linux
- **Processamento em Lote** — Processe um semestre inteiro de VTTs com um único comando

---

## Instalação

### Passo 1 — Instalar o Python

> **Já tem o Python?** Abra um terminal e execute `python3 --version` (Mac/Linux) ou `python --version` (Windows). Se aparecer `Python 3.x.x`, pule para o Passo 2.

**Windows**

1. Acesse **[python.org/downloads](https://www.python.org/downloads/)** e clique em "Download Python 3.x.x"
2. Execute o instalador
3. **Importante:** No rodapé do instalador, marque a opção **"Add python.exe to PATH"** antes de clicar em Install
4. Abra o **Prompt de Comando**: pressione `Win+R`, digite `cmd`, pressione Enter
5. Verifique: `python --version` → deve mostrar `Python 3.x.x`

> No Windows, use `python` no lugar de `python3` em todos os comandos abaixo.

**Mac**

1. Abra o **Terminal**: pressione `Cmd+Space`, digite `Terminal`, pressione Enter
2. Instale via Homebrew (recomendado):
   ```bash
   # Instale o Homebrew primeiro (se não tiver)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   # Depois instale o Python
   brew install python3
   ```
   Ou baixe o instalador direto em [python.org/downloads](https://www.python.org/downloads/)
3. Verifique: `python3 --version`

**Linux** (Ubuntu / Debian / Pop!\_OS)

```bash
sudo apt update && sudo apt install python3
```

Para Fedora / RHEL:
```bash
sudo dnf install python3
```

Verifique: `python3 --version`

---

### Passo 2 — Baixar o VTT-to-Insights

**Opção A — Via Git** (recomendado)

```bash
git clone https://github.com/maxh33/VTT-to-Insights.git
cd VTT-to-Insights
```

**Opção B — Download ZIP**

Clique no botão verde **Code** em [github.com/maxh33/VTT-to-Insights](https://github.com/maxh33/VTT-to-Insights) → **Download ZIP** → extraia a pasta.

Nenhum `pip install` é necessário — o script usa apenas bibliotecas nativas do Python.

---

## Início Rápido

### Execute o script

**Linux / Mac**
```bash
python3 vtt_clean.py "Minha Aula 04-02-2024.vtt"
```

**Windows (Prompt de Comando)**
```cmd
python vtt_clean.py "Minha Aula 04-02-2024.vtt"
```

**Windows (PowerShell)**
```powershell
python vtt_clean.py "Minha Aula 04-02-2024.vtt"
```

> **Dica:** Arraste e solte o arquivo `.vtt` na janela do terminal para colar o caminho completo automaticamente.

> **Dica Windows:** Se `python` não for reconhecido, tente `py vtt_clean.py "..."`.

**O que você verá no terminal:**

```
──────────────────────────────────────────────────────
  VTT-to-Insights  ·  Minha Aula 04-02-2024.vtt
──────────────────────────────────────────────────────
                            BEFORE        AFTER    SAVED
  Lines / blocks            11,247       166 blk
  Tokens (est.)            ~98,000      ~32,428      67%
  File size (KB)            381.3       126.7      67%
──────────────────────────────────────────────────────
  Saved : Minha Aula 04-02-2024_clean.txt
  Folder: /caminho/para/suas/aulas
  Next  : open a prompt from prompts/en/ or prompts/pt-BR/
          paste Minha Aula 04-02-2024_clean.txt into Claude / Gemini / ChatGPT
──────────────────────────────────────────────────────
```

Uma aula de 3 horas passa de ~98.000 tokens barulhentos para ~32.000 limpos — uma **redução de 67%** que cabe confortavelmente na janela de contexto de qualquer IA.

---

### Arquivo VTT em outra pasta

Você não precisa mover o arquivo `.vtt` para dentro do projeto. Passe o caminho completo do arquivo diretamente — o script funciona de qualquer lugar.

> **Dica:** Arraste e solte o arquivo `.vtt` na janela do terminal para colar o caminho completo automaticamente.
> **Dica:** Pressione `Tab` para autocompletar nomes de pastas e arquivos enquanto digita.

**Linux**
```bash
# Arquivo em ~/Documents
python3 ~/VTT-to-Insights/vtt_clean.py ~/Documents/aula.vtt

# Arquivo em pasta de nuvem ou drive montado
python3 ~/VTT-to-Insights/vtt_clean.py "/mnt/storage/Faculdade/1 Semestre/aula.vtt"
```

**Mac**
```bash
# Arquivo em Downloads
python3 ~/VTT-to-Insights/vtt_clean.py ~/Downloads/aula.vtt

# Arquivo em pasta de disciplina dentro de Documentos
python3 ~/VTT-to-Insights/vtt_clean.py "/Users/seunome/Documents/Faculdade/1 Semestre/aula.vtt"

# Arquivo no iCloud Drive
python3 ~/VTT-to-Insights/vtt_clean.py ~/Library/Mobile\ Documents/com~apple~CloudDocs/aula.vtt
```

**Windows (Prompt de Comando)**
```cmd
python C:\Users\SeuNome\VTT-to-Insights\vtt_clean.py "C:\Users\SeuNome\Downloads\aula.vtt"
python C:\Users\SeuNome\VTT-to-Insights\vtt_clean.py "C:\Users\SeuNome\Documents\Faculdade\1 Semestre\aula.vtt"
```

**Windows (PowerShell)**
```powershell
python C:\Users\SeuNome\VTT-to-Insights\vtt_clean.py "C:\Users\SeuNome\Downloads\aula.vtt"
python C:\Users\SeuNome\VTT-to-Insights\vtt_clean.py "C:\Users\SeuNome\Documents\Faculdade\1 Semestre\aula.vtt"
```

> **Sempre escreva o comando em uma única linha.** Dividir com `\` + Enter causa erro de "arquivo não encontrado" porque o shell adiciona um espaço no início do caminho.

> **Local do arquivo de saída:** O arquivo `_clean.txt` é salvo na mesma pasta do `.vtt` — não na pasta do projeto.

---

## Usando os Prompts

Depois que o script criar o arquivo `_clean.txt`:

1. **Abra** o `_clean.txt` em qualquer editor de texto (Bloco de Notas, TextEdit, VS Code) → **Selecionar Tudo** (`Ctrl+A` / `Cmd+A`) → **Copiar** (`Ctrl+C` / `Cmd+C`)
2. **Abra** um dos arquivos de prompt da pasta `prompts/pt-BR/` (ex: `prompts/pt-BR/study-notes.md`)
3. **Copie** o texto dentro do bloco ` ``` ` — esse é o seu prompt
4. Acesse **[claude.ai](https://claude.ai)** (ou chatgpt.com / gemini.google.com) → inicie um **Novo chat**
5. **Cole** o prompt na caixa de mensagem
6. Role até o final do prompt e **substitua** `[COLE O CONTEÚDO DO _clean.txt AQUI]` pela transcrição que você copiou no passo 1
7. **Envie** — aguarde ~30 segundos — suas anotações estruturadas aparecem

---

## Biblioteca de Prompts

| Prompt | Idioma | Quando Usar | Tempo de Leitura |
|--------|--------|-------------|------------------|
| [`prompts/pt-BR/study-notes.md`](prompts/pt-BR/study-notes.md) | 🇧🇷 Português | Análise acadêmica completa (5 seções) | ~5 min |
| [`prompts/pt-BR/quick-summary.md`](prompts/pt-BR/quick-summary.md) | 🇧🇷 Português | Resumo rápido em 5 pontos | ~1 min |
| [`prompts/pt-BR/concepts-only.md`](prompts/pt-BR/concepts-only.md) | 🇧🇷 Português | Glossário de conceitos | ~3 min |
| [`prompts/en/study-notes.md`](prompts/en/study-notes.md) | 🇬🇧 English | Full 5-section academic analysis | ~5 min |
| [`prompts/en/quick-summary.md`](prompts/en/quick-summary.md) | 🇬🇧 English | 5-bullet quick overview | ~1 min |
| [`prompts/en/concepts-only.md`](prompts/en/concepts-only.md) | 🇬🇧 English | Concept glossary | ~3 min |

Veja [`examples/sample_output.md`](examples/sample_output.md) para um exemplo real do que a IA produz.

---

## Formato de Saída

O arquivo limpo tem um bloco de parágrafo por ~60 segundos, cada um com um timestamp:

```
[00:03:10] A partir de hoje a gente vai começar um pouco teórico,
como construir ali um conhecimento para depois desse conhecimento,
tendo aquela base estruturada, a gente consiga fazer colocar em
prática ali. A gente vai mexer com Figma...

[00:05:11] O fundamento de IHC é a organização e arquitetura
aplicada ao computador humano. Interação humano computador...
```

---

## Todas as Opções

```
python3 vtt_clean.py [OPÇÕES] arquivo.vtt

argumentos posicionais:
  vtt_file              Caminho para o arquivo .vtt

opções:
  --block-seconds N     Segundos por bloco de parágrafo (padrão: 60)
  --output ARQUIVO, -o  Caminho personalizado para o arquivo de saída
  --stdout              Imprime na saída padrão (útil para pipes)
  -h, --help            Mostra esta ajuda
```

**Mais exemplos:**

```bash
# Blocos maiores — menos fragmentados, melhor para monólogos longos
python3 vtt_clean.py aula.vtt --block-seconds 90

# Salvar em local específico (Linux/Mac)
python3 vtt_clean.py aula.vtt --output ~/Desktop/aula_limpa.txt

# Salvar em local específico (Windows)
python vtt_clean.py aula.vtt --output "C:\Users\Você\Desktop\aula_limpa.txt"

# Copiar output direto para a área de transferência (Mac)
python3 vtt_clean.py aula.vtt --stdout | pbcopy

# Copiar output direto para a área de transferência (Linux)
python3 vtt_clean.py aula.vtt --stdout | xclip -selection clipboard

# Processar todas as VTTs de uma pasta (Linux/Mac)
for f in aulas/*.vtt; do python3 vtt_clean.py "$f"; done

# Processar todas as VTTs de uma pasta (Windows PowerShell)
Get-ChildItem -Filter *.vtt | ForEach-Object { python vtt_clean.py $_.FullName }
```

---

## Notas por Plataforma

| Plataforma | Comando Python | Como abrir o terminal |
|------------|---------------|----------------------|
| Windows | `python` ou `py` | Prompt de Comando (`cmd`) ou PowerShell |
| Mac | `python3` | Terminal (Cmd+Space → "Terminal") |
| Linux | `python3` | Terminal da sua distro |

> **Dica Windows com espaços no caminho:** Use aspas: `python vtt_clean.py "C:\Minhas Aulas\semana1.vtt"`

---

## Compatibilidade de Origem do VTT

Testado com arquivos VTT exportados de:
- **Microsoft Teams** (portais universitários, reuniões gravadas)
- **Zoom** (legendas geradas automaticamente)
- **Google Meet** (com gravação de legendas habilitada)
- **YouTube** (auto-geradas — baixe com `yt-dlp --write-auto-sub --sub-lang pt URL`)

---

## Estrutura do Projeto

```
VTT-to-Insights/
├── vtt_clean.py               ← Script principal (sem dependências)
├── prompts/
│   ├── pt-BR/                 ← Prompts em Português
│   │   ├── study-notes.md
│   │   ├── quick-summary.md
│   │   └── concepts-only.md
│   └── en/                    ← Prompts em Inglês
│       ├── study-notes.md
│       ├── quick-summary.md
│       └── concepts-only.md
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
- Mais templates de prompt (preparação para prova, mapas mentais)
- Traduções para outros idiomas

Abra uma issue ou envie um PR em [github.com/maxh33/VTT-to-Insights](https://github.com/maxh33/VTT-to-Insights).

---

## Licença

MIT — veja [LICENSE](LICENSE)

---

*Este projeto nasceu numa sala de aula de Ciência da Computação no Brasil 🇧🇷 para ajudar estudantes do mundo todo a lidar com transcrições longas de aula. Contribuições são bem-vindas!*

# Workaround: Transcrever Aulas MS Teams Live Events

Algumas aulas são transmitidas via **MS Teams Live Events** (modo broadcast). Nesse modo, o organizador controla completamente a gravação e transcrição — participantes externos **não conseguem** baixar `.vtt`, `.docx` nem iniciar transcrição nativa.

Este guia documenta como capturar e transcrever essas aulas usando OBS + LocalVocal localmente, sem depender do organizador.

---

## O que você vai precisar

| Ferramenta | Finalidade | Download |
|---|---|---|
| **OBS Studio** | Captura de áudio | [obsproject.com](https://obsproject.com/) |
| **LocalVocal** (plugin OBS) | Transcrição em tempo real com Whisper | [releases](https://github.com/locaal-ai/obs-localvocal/releases) |
| **Python 3** | Scripts de conversão/transcrição | já incluso no projeto |

> **GPU NVIDIA**: instale a versão `nvidia` do LocalVocal (`obs-localvocal-x.x.x-windows-x64-nvidia-Installer.exe`). Permite usar modelos `large-v3` em tempo real.

---

## Configuração no OBS (fazer uma única vez)

### 1. Adicionar fonte de áudio isolada

Adicione uma fonte do tipo **Application Audio Capture**:
- Clique em `+` na caixa **Fontes** → **Application Audio Capture**
- Selecione o browser onde o Teams está aberto (ex: **Google Chrome** ou **Microsoft Edge**)

Isso captura **apenas o áudio do browser**, ignorando outros apps do sistema.

> Enquanto a aula rolar, mantenha só a aba do Teams aberta no browser para evitar capturar outros sons.

### 2. Adicionar o filtro LocalVocal

- Clique no ícone de mixer/engrenagem da fonte de áudio criada
- **Adicionar Filtro → LocalVocal (Captions)**

### 3. Configurar o LocalVocal

| Opção | Valor recomendado |
|---|---|
| Language | `Portuguese` |
| Model | `large-v3` (Whisper built-in) — melhor para PT-BR, ~4GB VRAM |
| Output to file | ✅ Ativar → definir caminho do `.srt` (ex: `C:\aulas\transcricao.srt`) |
| Add WebVTT captions to recording | ✅ Opcional — embute legenda no vídeo gravado pelo OBS (bom como backup) |
| Add WebVTT captions to stream | ❌ Não — só para quem está transmitindo via RTMP |

> **Sobre modelos**: `large-v3` é excelente para Português BR. Com RTX 3070 ou superior, roda em tempo real sem problema. Se quiser ainda mais precisão para sotaque BR, existe o modelo [`Gustrd/whisper-medium-portuguese-ggml-model`](https://huggingface.co/Gustrd/whisper-medium-portuguese-ggml-model) no HuggingFace (download manual).

---

## Durante a aula

1. Abra o OBS antes de entrar na aula
2. Verifique que o **medidor de áudio** da fonte de áudio se move ao som do Teams
3. O LocalVocal transcreve automaticamente em tempo real
4. Ao fim da aula: o arquivo `.srt` está pronto em `C:\aulas\transcricao.srt`

> Sessões de 3h+: sem problema. O LocalVocal escreve no arquivo incrementalmente (processa chunks de ~30s), sem acumular em memória.

---

## Após a aula: converter SRT → VTT e processar

O LocalVocal gera `.srt`. O pipeline VTT-to-Insights espera `.vtt`. A conversão é simples:

```bash
# Copiar o SRT para o projeto (ou montar no WSL: /mnt/c/aulas/transcricao.srt)
python3 scripts/srt_to_vtt.py /mnt/c/aulas/transcricao.srt

# O arquivo transcricao.vtt é gerado no mesmo diretório
# Agora processar com o pipeline normal:
python3 scripts/vtt_clean.py /mnt/c/aulas/transcricao.vtt
```

---

## Alternativa: Transcrever uma gravação já disponível

Se o professor disponibilizou o vídeo da aula depois:

```bash
# Instalar faster-whisper (uma vez)
pip install faster-whisper

# Transcrever diretamente para VTT (usa GPU NVIDIA automaticamente)
python3 scripts/transcribe.py aula.mp4

# Processar com o pipeline
python3 scripts/vtt_clean.py aula.vtt
```

Modelos disponíveis: `tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3` (padrão).

---

## Fluxo completo resumido

```
MS Teams Live Event (browser)
         │
         ▼
OBS + Application Audio Capture (Chrome/Edge)
         │
         ▼
LocalVocal filter (Whisper large-v3, Português)
         │
         ▼
transcricao.srt  ←── arquivo gerado em tempo real durante a aula
         │
         ▼
python3 scripts/srt_to_vtt.py transcricao.srt
         │
         ▼
transcricao.vtt
         │
         ▼
python3 scripts/vtt_clean.py transcricao.vtt
         │
         ▼
transcricao_clean.txt  →  colar no Claude / Gemini / ChatGPT
```

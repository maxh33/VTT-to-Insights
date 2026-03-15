# LocalVocal — Configurações recomendadas para reduzir alucinações

## Problema: repetições de palavras (alucinação do ASR)

O Whisper (especialmente Large V3) pode entrar em loop e gerar repetições como:

> "décadas, décadas, décadas, décadas, décadas"

Isso ocorre quando a inferência é interrompida brevemente — comum com o backend **Vulkan no Windows** ao tirar screenshots (Snipping Tool, ShareX com GPU capture, etc.), que causam um spike de GPU e stall na inferência.

Referência: [whisper.cpp issue #3351](https://github.com/ggerganov/whisper.cpp/issues/3351)

O script `vtt_clean.py` remove essas repetições automaticamente e exibe um aviso `⚠` no terminal com o timestamp, para que você possa revisar o trecho no vídeo original se necessário.

---

## Configurações recomendadas

| Parâmetro | Atual | Recomendado | Motivo |
|-----------|-------|-------------|--------|
| Entropy threshold | 1.00 | **2.0–2.2** | 1.00 rejeita fala válida; 2.4 é o default do Whisper |
| Logprob threshold | 0.00 | **-1.0** | 0.00 é muito restritivo; o default é -1.0 |
| Beam size | 5 | **1** | Beam alto aumenta alucinações em real-time (ver pesquisa abaixo) |
| Greedy best of | 1 | **3** | Avalia 3 candidatos, reduz loops sem o custo do beam search |
| Temperature increment | 0.20 | **0.10** | Fallback mais gradual, menos "criativo" |
| Temperature | 0.05 | **0.05** | Manter — excelente para transcrição |
| Partial Transcription | 1100ms | **desativar ou 2000ms+** | Reduz carga GPU; menos risco de stall durante screenshots |
| Suppress regex | (vazio) | `(décadas\s*,?\s*){3,}` | Filtro de emergência inline (opcional) |

### O que NÃO mudar

| Parâmetro | Valor | Motivo |
|-----------|-------|--------|
| VAD Mode | Active VAD | Filtra silêncios — principal causa de alucinação |
| VAD Threshold | 0.65 | Adequado |
| Initial prompt | "assuntos relacionados ao curso de ciencia da computacao" | Ancora o modelo no domínio |
| No context | ✓ checked | Previne amplificação de contexto incorreto |

---

## Por que beam size alto causa mais alucinações em real-time?

Em transcrição em tempo real, o modelo recebe chunks de áudio pequenos e incompletos. Com beam search (beam > 1), o modelo explora múltiplas hipóteses e pode "comprometer-se" com uma sequência de tokens incorreta baseada em áudio parcial. Com greedy search (beam = 1), o modelo toma decisões mais conservadoras e é menos propenso a entrar em loops.

Referências:
- [Whisper hallucination paper (Koenecke et al., 2024)](https://arxiv.org/abs/2309.15806)
- [whisper.cpp: beam search increases hallucinations #1729](https://github.com/ggerganov/whisper.cpp/issues/1729)

---

## Workaround imediato para screenshots

Evite ferramentas de screenshot que usam aceleração GPU durante a gravação:

| Ferramenta | Impacto GPU | Recomendação |
|-----------|-------------|--------------|
| `Win + Shift + S` (Snip & Sketch) | Baixo (CPU) | **Preferir** |
| Snipping Tool moderno | Médio | Usar com cuidado |
| ShareX com GPU capture | Alto | Evitar durante gravação |
| OBS replay buffer | Alto | Evitar durante transcrição |

---

## Configuração de referência do LocalVocal (após ajustes)

```
Model:              Whisper Large V3
Backend:            Vulkan
Temperature:        0.05
Temperature inc:    0.10
Beam size:          1
Greedy best of:     3
Entropy threshold:  2.1
Logprob threshold:  -1.0
VAD Mode:           Active VAD
VAD Threshold:      0.65
No context:         ✓
Initial prompt:     assuntos relacionados ao curso de ciencia da computacao
Partial transcr.:   desativado (ou 2000ms+)
```

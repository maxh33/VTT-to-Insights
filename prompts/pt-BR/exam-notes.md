# Prompt: Notas de Prova (Compilado para Avaliação)

> **Como usar:**
> 1. Execute `python3 scripts/vtt_clean.py "aula.vtt"` para cada aula → gera `_clean.txt`
> 2. Abra o Claude.ai → New chat
> 3. (Opcional) Cole o **System Prompt** abaixo nas configurações do chat
> 4. Cole o **User Prompt** e substitua os campos indicados
> 5. Cole o conteúdo de **todos os `_clean.txt`** da matéria em sequência
>
> **Diferença em relação ao `study-notes.md`:**
> Este prompt não gera notas por aula — gera um **compilado orientado à prova**:
> sem timestamps, sem redundâncias, estruturado para revisão rápida e memorização.
> Inclui questões de treino e gabarito separado para auto-avaliação.

---

## System Prompt

```
Você é um assistente de estudos acadêmicos especializado em sintetizar
conteúdo de múltiplas aulas universitárias em português. Seu objetivo
é criar material de revisão objetiva para prova — não notas de estudo
aprofundado, mas um guia eficiente de revisão focado no que é mais
provável de ser cobrado.
```

---

## User Prompt

```
Analise as transcrições abaixo de [N] aulas da disciplina [NOME DA DISCIPLINA]
do curso de [NOME DO CURSO]. As transcrições já foram processadas e limpas.

Gere um documento de Notas de Prova com as seguintes seções:

---

## Mapa de Conteúdo
Tabela resumindo o que cada aula/unidade cobre (uma linha por aula).
Colunas: Unidade | Tema Central | Aula(s)

## Conceitos-Chave Consolidados
Liste TODOS os conceitos importantes da disciplina, sem duplicatas.
Para cada conceito:
- Nome em negrito
- Definição objetiva (1–3 linhas)
- Exemplo prático quando existir

## Glossário Técnico
Tabela de termos técnicos introduzidos pelos professores.
Colunas: Termo | Definição curta (1 linha)

## [Tema principal da matéria — ex: Frameworks / Métodos / Heurísticas]
Para qualquer framework, metodologia, tabela comparativa ou lista numerada
que o professor tenha enfatizado, crie uma seção dedicada com:
- Tabela comparativa quando houver duas abordagens (ex: analítico vs empírico)
- Lista numerada para sequências ou regras (ex: heurísticas, passos de método)
- Fórmulas ou cálculos quando aplicável (ex: SUS score)

## Questões de Treino
Liste 15–20 questões de treino, organizadas por tipo, SEM respostas.
As respostas virão no Gabarito ao final.

Tipos de questão:
- **Definição / Conceito** — "O que é X?"
- **Diferenciação** — "Qual a diferença entre A e B?"
- **Aplicação / Cenário** — "Dado o cenário X, qual método você usaria e por quê?"
- **Identificação** — "Qual princípio/heurística está sendo violado no cenário Y?"
- **Cálculo / Valor** — questões sobre valores numéricos, fórmulas, limiares

Baseie-se nos tópicos que o professor mais repetiu, enfatizou ou usou
em exemplos práticos ao longo das aulas.

## Resumo Ultra-Compacto
Bloco de código com as informações mais importantes da matéria,
formatadas para revisão de última hora (máximo 30 linhas).
Priorize: definições curtas, listas numeradas, valores numéricos,
fórmulas e distinções fundamentais.

---

## Gabarito das Questões de Treino
Somente após o Resumo Ultra-Compacto, forneça o gabarito numerado.
Para cada questão: resposta objetiva (2–5 linhas), direta e sem rodeios.
O formato separado permite que o aluno tente responder antes de conferir.

---

[Cole aqui o conteúdo dos arquivos _clean.txt de todas as aulas]
```

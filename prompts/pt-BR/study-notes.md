# Prompt: Análise Completa de Aula (Estudo Acadêmico)

> **Como usar:**
> 1. Execute `python3 vtt_clean.py "sua_aula.vtt"` para gerar o `_clean.txt`
> 2. Abra o Claude.ai → New chat
> 3. (Opcional) Cole o **System Prompt** abaixo nas configurações do chat
> 4. Cole o **User Prompt** e substitua `[NOME DA DISCIPLINA]`
> 5. Cole o conteúdo do `_clean.txt` onde indicado

---

## System Prompt

```
Você é um assistente de estudos acadêmicos especializado em analisar
transcrições de aulas universitárias em português. Seu objetivo é
extrair o máximo de valor de estudo de cada aula.
```

---

## User Prompt

```
Analise a transcrição abaixo de uma aula de ~3 horas do curso de
Ciência da Computação (disciplina: [NOME DA DISCIPLINA]).

Produza uma análise estruturada com as seguintes seções:

## 📋 Índice de Tópicos
Liste cada tópico principal com o timestamp onde começa.
Formato: `[HH:MM:SS]` — Tópico

## 🔑 Conceitos-Chave
Liste todas as definições, conceitos, frameworks e termos técnicos
introduzidos. Para cada um, inclua:
- O nome do conceito em negrito
- Uma definição clara e objetiva
- O timestamp da explicação

## ⭐ Momentos Essenciais (Top 8–12)
Aponte os timestamps de maior valor de estudo — onde a professora
explica algo crítico, dá um exemplo prático ou demonstra uma técnica.
Para cada momento:
- Timestamp
- Uma frase explicando por que esse momento é importante

## 📝 Atividades e Exercícios
Liste qualquer tarefa, atividade prática ou exercício mencionado,
com o timestamp e contexto suficiente para entender o que fazer.

## 📖 Resumo da Aula
Resumo conciso de 250–350 palavras cobrindo:
- Tema central da aula
- Principais conceitos apresentados
- Conexões entre os tópicos
- O que foi prático vs. teórico

---
TRANSCRIÇÃO:
[COLE O CONTEÚDO DO _clean.txt AQUI]
```

# Workflow Completo: Study Notes + Notas de Prova (Claude Code)

> **Objetivo:** pipeline reutilizável para qualquer matéria e semestre.
> Siga as fases em ordem — cada fase depende da anterior.

---

## Variáveis — defina antes de começar

```bash
SCRIPTS="/mnt/d/Programacao/Repositorios/VTT-to-Insights/scripts"
MATERIA="/mnt/d/Programacao/Repositorios/cs-cruzeiro-do-sul/01-semestre/<disciplina>"
AULAS="$MATERIA/aulas"
```

---

## Fase 1 — Processar SRTs das aulas (repetir para cada aula nova)

SRTs do OBS LocalVocal frequentemente têm nomes com encoding corrompido.
Usar Python por índice para localizar.

```bash
# 1a. Listar arquivos para achar o SRT pelo índice
python3 -c "
import os
for i, f in enumerate(os.listdir('$AULAS/')):
    print(i, repr(f))
"

# 1b. SRT → VTT (substituir N pelo índice correto)
python3 -c "
import os, subprocess, sys
fname = os.listdir('$AULAS/')[N]
subprocess.run([sys.executable, '$SCRIPTS/srt_to_vtt.py',
    '$AULAS/' + fname, '--output', '$AULAS/aula-NN-DDmes.vtt'])
"

# 1c. VTT → _clean.txt
python3 "$SCRIPTS/vtt_clean.py" \
  "$AULAS/aula-NN-DDmes.vtt" \
  --output "$AULAS/aula-NN-DDmes_clean.txt"

# 1d. Ler o _clean.txt para determinar o tópico e renomear os dois arquivos:
#   mv aula-NN-DDmes.vtt          aula-NN-DDmes-<topico>.vtt
#   mv aula-NN-DDmes_clean.txt    aula-NN-DDmes-<topico>_clean.txt
```

**Convenção de nomes:** `aula-NN-DDmes-<topico-slug>_clean.txt`
Ex: `aula-03-23mai-estruturas-condicionais-if-elif-else_clean.txt`

---

## Fase 2 — Gerar Study Notes por aula (`_study_notes.md`)

Para cada `_clean.txt` existente, pedir ao Claude Code:

```
Leia o arquivo:
$AULAS/aula-NN-DDmes-<topico>_clean.txt

Gere notas de estudo completas e salve como:
$AULAS/aula-NN-DDmes-<topico>_study_notes.md

O arquivo deve conter:
1. Título com número e data da aula
2. Tópicos cobertos (lista)
3. Conceitos-chave — para cada: definição objetiva + exemplo de código quando aplicável
4. Tabelas comparativas para abordagens/estruturas diferentes
5. Exercícios resolvidos com código comentado (se houver na aula)
6. Resumo Ultra-Compacto — bloco de código, máximo 20 linhas

Priorize o que a professora repetiu, enfatizou e usou em exemplos práticos.
Não inclua timestamps. Foque no conteúdo técnico.
```

**Resultado esperado:** um `_study_notes.md` por `_clean.txt`.

---

## Fase 3 — Gerar Notas de Prova finais

Com todas as fases anteriores completas, pedir ao Claude Code:

```
Gere as Notas de Prova para a matéria em:
$MATERIA/

Leia de forma autônoma, nesta ordem de prioridade:
1. avisos.txt — prazos, composição de nota, datas de prova
2. Todos os aulas/*_study_notes.md — notas de estudo já geradas
3. Todos os aulas/*_clean.txt — transcrições (complemento)
4. Todos os material/*.txt — textos formais das unidades
5. Todos os atividades/**/devolutiva*.txt — feedback das entregas
6. Todos os atividades/**/context*.txt — brief das atividades

Salve o resultado como:
$MATERIA/prova-<nome-disciplina>.md

Com as seguintes seções:

1. **Mapa de Conteúdo** — tabela: Unidade | Tema Central | Aula(s) | Status

2. **Conceitos-Chave Consolidados** — todos os conceitos importantes,
   sem duplicatas. Para cada: nome em negrito, definição objetiva (1-3 linhas),
   exemplo prático quando existir.

3. **Glossário Técnico** — tabela: Termo | Definição (1 linha)

4. **[Seção temática específica]** — adaptada ao conteúdo da matéria:
   - Tabelas comparativas para estruturas/abordagens opostas
   - Listas numeradas para sequências e regras
   - Blocos de código para sintaxe importante
   - Fórmulas ou valores numéricos que o professor enfatizou

5. **Pontos de Atenção** — baseado nas devolutivas das atividades:
   o que o professor corrigiu, valorizou e vai cobrar na prova.
   (Incluir apenas se existirem devolutivas com feedback substantivo)

6. **Conexões Importantes** — como os temas se relacionam entre si
   (útil para questões de aplicação e cenário)

7. **Questões de Treino** — 15-20 questões SEM respostas, por tipo:
   Definição/Conceito | Diferenciação | Aplicação/Cenário | Cálculo/Código

8. **Resumo Ultra-Compacto** — bloco de código, máximo 30 linhas,
   para revisão de última hora.

9. **Gabarito** — somente após o Resumo, respostas numeradas
   (2-5 linhas cada). Formato separado para treino ativo.

Priorize o que a professora mais repetiu e usou em exemplos práticos.
Não inclua timestamps. Foque no conteúdo técnico.
```

---

## Checklist por matéria

| Fase | Arquivo gerado | Commitar? |
|------|---------------|-----------|
| 1 — SRT→VTT | `aula-NN-DDmes-<topico>.vtt` | Não (ignorado) |
| 1 — VTT→clean | `aula-NN-DDmes-<topico>_clean.txt` | **Sim** |
| 2 — Study notes | `aula-NN-DDmes-<topico>_study_notes.md` | **Sim** |
| 3 — Notas de prova | `prova-<disciplina>.md` | **Sim** |

```bash
# Commitar todos os .md e _clean.txt de uma vez (nunca usar git add .)
git add 01-semestre/<disciplina>/aulas/*_clean.txt
git add 01-semestre/<disciplina>/aulas/*_study_notes.md
git add 01-semestre/<disciplina>/prova-*.md
git commit -m "docs(<disciplina>): add study notes and exam notes for all aulas"
```

---

## Dicas

- **Matéria nova:** começar pela Fase 1 para cada SRT gravado
- **Aula nova no meio do semestre:** rodar apenas Fase 1 + Fase 2 para ela, depois regerar a Fase 3
- **Pré-prova urgente:** se não tiver tempo para Fase 2, ir direto à Fase 3 passando os `_clean.txt`
- **Contexto grande demais:** usar `gemini -p "@$MATERIA/ Gere notas de prova..."` como alternativa

# Prompt: Notas de Prova via Claude Code (path-based)

> **Diferença em relação ao `exam-notes.md`:**
> Este prompt é para uso no **Claude Code (CLI)** — você passa o caminho da pasta
> da matéria e o Claude lê todos os arquivos relevantes automaticamente.
> Não é necessário copiar e colar nenhum conteúdo.

---

## Como usar

```bash
# No terminal, inicie o Claude Code na raiz do repositório
claude

# Em seguida, envie a mensagem abaixo substituindo o caminho:
```

## Mensagem para o Claude Code

```
Gera as Notas de Prova para a matéria em:
[CAMINHO_DA_PASTA_DA_MATERIA]
Ex: 01-semestre/interface-jornada-usuario/

Leia de forma autônoma os seguintes arquivos da pasta:
- Todos os _clean.txt em aulas/
- Todos os .md de notas de estudo em aulas/
- Todos os .txt em material/ (exceto binários)
- O arquivo avisos.txt na raiz da pasta da matéria

Com base nesse conteúdo, gere um arquivo Markdown chamado
"Notas de Prova_ [NOME DA DISCIPLINA].md" dentro de aulas/
com as seguintes seções:

1. **Mapa de Conteúdo** — tabela: Unidade | Tema Central | Aula(s)

2. **Conceitos-Chave Consolidados** — todos os conceitos importantes,
   sem duplicatas. Para cada: nome em negrito, definição objetiva (1-3 linhas),
   exemplo prático quando existir.

3. **Glossário Técnico** — tabela: Termo | Definição curta (1 linha)

4. **[Seção específica do conteúdo]** — para frameworks, métodos, listas
   numeradas ou tabelas comparativas que o professor enfatizou:
   - Tabelas comparativas para abordagens opostas
   - Listas numeradas para sequências/regras
   - Fórmulas ou valores numéricos importantes

5. **Conexões Importantes** — como os temas se relacionam entre si
   (útil para questões de aplicação/cenário)

6. **Questões de Treino** — 15-20 questões SEM respostas, organizadas por tipo:
   - Definição/Conceito, Diferenciação, Aplicação/Cenário,
     Identificação de violação, Cálculo/Valor

7. **Resumo Ultra-Compacto** — bloco de código, máximo 30 linhas,
   para revisão de última hora. Definições curtas, listas, valores numéricos,
   distinções fundamentais.

8. **Gabarito das Questões de Treino** — somente após o Resumo,
   respostas numeradas (2-5 linhas cada), diretas e sem rodeios.
   O formato separado permite treino ativo antes de conferir.

Priorize o que os professores mais repetiram, enfatizaram ou usaram
em exemplos práticos. Não inclua timestamps — foque no conteúdo.
```

---

## Dicas de uso

- **Matéria com muitas aulas:** passe também os arquivos `_clean.txt` mais relevantes explicitamente se quiser priorizar certas aulas
- **Pré-prova:** peça também `"adicione uma seção de Pontos de Atenção baseado nas devolutivas das atividades"` se houver feedbacks nas atividades
- **Resultado:** o arquivo gerado ficará em `aulas/Notas de Prova_ [matéria].md` — pronto para revisar ou commitar

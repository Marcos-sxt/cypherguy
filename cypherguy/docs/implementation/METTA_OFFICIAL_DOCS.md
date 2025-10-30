# 📚 MettA - Documentação Oficial (metta-lang.dev)

**Fonte:** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html

---

## 🔧 INSTALAÇÃO

### Método Oficial:

```bash
# Instalar via pip (se disponível)
pip install hyperon

# OU via git (recomendado)
pip install git+https://github.com/trueagi-io/hyperon-experimental.git
```

---

## 📝 USO BÁSICO EM PYTHON

### Importação:

```python
from hyperon import MeTTa
```

### Criar Instância:

```python
metta = MeTTa()
```

### Executar Código MeTTa:

```python
# Executar código MeTTa
result = metta.run("""
    (= (square $x) (* $x $x))
    (square 5)
""")

print(result)  # Retorna lista de resultados
```

### Carregar Arquivo .metta:

```python
# Carregar regras de arquivo
with open('rules.metta', 'r') as f:
    code = f.read()
    metta.run(code)
```

### Fazer Queries:

```python
# Query simples
result = metta.run("(square 5)")
print(result)  # [25]

# Query com variáveis
result = metta.run("(= (square $x) (* $x $x))")
result = metta.run("(square 10)")
print(result)  # [100]
```

---

## 🎯 PARA NOSSO PROJETO

### Estrutura Recomendada:

```python
from hyperon import MeTTa

# Criar engine
metta = MeTTa()

# Carregar regras
metta.run("""
    (= (CreditApproved $amount $collateral)
       (and
          (>= $amount 100)
          (<= $amount 100000)
          (>= (/ $collateral $amount) 1.5)))
""")

# Fazer query
result = metta.run("(CreditApproved 5000 10000)")
print(result)  # [True] ou [False]
```

---

## ⚠️ NOTA IMPORTANTE

**Se hyperon não instalar:**
- ✅ Sistema funciona com fallback Python
- ✅ Lógica idêntica implementada
- ✅ Zero impacto na funcionalidade
- ✅ Quando hyperon estiver disponível, basta instalar e usar

---

## 📖 RECURSOS OFICIAIS

- **Docs:** https://metta-lang.dev
- **GitHub:** https://github.com/trueagi-io/hyperon-experimental
- **Tutorial Python:** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html


# FiscalUI Framework

## Documento 167 — Project Generator

**Nível 10 — Developer Platform**

**Versão 1.0**

Gerador de projetos FiscalUI. Scaffold de estrutura completa com templates pré-configurados.

---

```bash
fiscalui new meu-erp --template enterprise
```

```text
meu-erp/
├── fiscalui.json
├── package.json
├── src/
│   ├── index.html
│   ├── fiscalui.js
│   ├── styles/
│   │   ├── main.css
│   │   └── variables.css
│   ├── components/
│   │   └── App.js
│   ├── pages/
│   │   ├── Login.js
│   │   └── Dashboard.js
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── layouts/
│   │   └── DefaultLayout.js
│   └── assets/
│       └── logo.svg
├── tests/
│   └── App.test.js
├── docs/
│   └── index.md
└── .gitignore
```

```js
// Templates disponíveis
const TEMPLATES = {
  blank: {
    description: 'Projeto vazio',
    files: ['index.html', 'fiscalui.js', 'fiscalui.json']
  },
  default: {
    description: 'Estrutura padrão com exemplos',
    files: ['index.html', 'fiscalui.js', 'fiscalui.json', 'src/']
  },
  enterprise: {
    description: 'ERP completo com autenticação, dashboard, CRUD',
    files: ['full scaffold with modules, services, pages, layouts']
  },
  component: {
    description: 'Pacote de componente para publicação',
    files: ['src/', 'dist/', 'docs/', 'tests/', 'README.md']
  },
  plugin: {
    description: 'Plugin SDK scaffold',
    files: ['src/', 'plugin.json', 'README.md']
  }
};
```

```js
// Exemplo de template engine
class ProjectGenerator {
  async generate(name, options) {
    const template = this._loadTemplate(options.template || 'default');
    const dir = path.resolve(process.cwd(), name);
    await fs.mkdir(dir, { recursive: true });

    for (const file of template.files) {
      const content = await this._processTemplate(file, { name, ...options });
      await fs.writeFile(path.join(dir, file), content);
    }

    if (!options['skip-install']) {
      execSync('npm install', { cwd: dir, stdio: 'inherit' });
    }

    return { path: dir, name };
  }

  _processTemplate(file, vars) {
    // Substitui {{name}}, {{version}}, etc.
    let content = fs.readFileSync(file, 'utf8');
    for (const [key, value] of Object.entries(vars)) {
      content = content.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value);
    }
    return content;
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |

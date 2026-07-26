# FiscalUI Framework

## Documento 170 — Theme SDK

**Nível 10 — Developer Platform**

**Versão 1.0**

SDK para criação de temas. Define tokens, variáveis CSS, componentes estilizados e paletas.

---

```json
// theme.json — manifesto do tema
{
  "name": "fiscalui-theme-corporate",
  "version": "1.0.0",
  "fiscalui": { "minVersion": "1.0.0", "type": "theme" },
  "description": "Tema corporativo azul escuro",
  "author": "Dev Name",
  "colors": {
    "primary": "#1a237e",
    "secondary": "#283593",
    "success": "#2e7d32",
    "warning": "#f57f17",
    "danger": "#c62828",
    "info": "#0277bd"
  },
  "typography": {
    "fontFamily": "'Inter', sans-serif",
    "headingFont": "'Inter', sans-serif",
    "fontSizeBase": "14px",
    "lineHeight": 1.5
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px"
  },
  "borderRadius": {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px"
  },
  "shadows": {
    "sm": "0 1px 3px rgba(0,0,0,0.12)",
    "md": "0 4px 6px rgba(0,0,0,0.15)",
    "lg": "0 10px 25px rgba(0,0,0,0.2)"
  }
}
```

```js
// ThemeSDK
class ThemeSDK {
  constructor(manifest) {
    this.manifest = manifest;
  }

  generateCSS() {
    const { colors, typography, spacing, borderRadius, shadows } = this.manifest;
    let css = ':root {\n';

    for (const [name, value] of Object.entries(colors)) {
      css += `  --color-${name}: ${value};\n`;
      css += `  --color-${name}-light: ${this._lighten(value, 30)};\n`;
      css += `  --color-${name}-dark: ${this._darken(value, 20)};\n`;
    }

    for (const [name, value] of Object.entries(spacing)) {
      css += `  --spacing-${name}: ${value};\n`;
    }

    for (const [name, value] of Object.entries(borderRadius || {})) {
      css += `  --radius-${name}: ${value};\n`;
    }

    for (const [name, value] of Object.entries(shadows || {})) {
      css += `  --shadow-${name}: ${value};\n`;
    }

    if (typography) {
      css += `  --font-family: ${typography.fontFamily};\n`;
      css += `  --font-size-base: ${typography.fontSizeBase};\n`;
      css += `  --line-height: ${typography.lineHeight};\n`;
    }

    css += '}\n';
    return css;
  }

  apply() {
    const style = document.createElement('style');
    style.id = `theme-${this.manifest.name}`;
    style.textContent = this.generateCSS();
    document.head.appendChild(style);
  }

  _lighten(hex, percent) { /* parse hex, lighten by percent */ }
  _darken(hex, percent) { /* parse hex, darken by percent */ }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |

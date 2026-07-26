# FiscalUI Framework

## Documento 179 — Deployment Tools

**Nível 10 — Developer Platform**

**Versão 1.0**

Ferramentas de build, empacotamento e deploy para produção.

---

```bash
fiscalui build                    # Build de produção
fiscalui build --minify           # Com minificação
fiscalui build --analyze          # Bundle analysis
fiscalui deploy                   # Deploy automático
fiscalui deploy --target s3       # AWS S3
fiscalui deploy --target vercel   # Vercel
fiscalui deploy --target netlify  # Netlify
fiscalui deploy --target custom   # Custom endpoint
```

```js
// Build configuration (fiscalui.json)
{
  "build": {
    "outDir": "dist",
    "publicPath": "/",
    "minify": {
      "html": true,
      "css": true,
      "js": true
    },
    "sourceMaps": true,
    "bundle": {
      "splitChunks": true,
      "vendor": ["fiscalui-core"],
      "async": true
    },
    "assets": {
      "images": "assets/images",
      "fonts": "assets/fonts",
      "icons": "assets/icons"
    },
    "pwa": {
      "enabled": true,
      "serviceWorker": true,
      "manifest": true
    }
  }
}
```

```js
// Build Pipeline
class BuildPipeline {
  constructor(config) {
    this.config = config;
  }

  async build() {
    const start = Date.now();
    Logger.info('🚀 Iniciando build...');

    // 1. Limpa diretório de saída
    await this._clean();

    // 2. Processa CSS (variáveis, vendor prefixes, minify)
    const css = await this._processCSS();

    // 3. Processa JS (bundle, transpile, minify)
    const js = await this._processJS();

    // 4. Processa HTML (template, inject assets)
    const html = await this._processHTML(css, js);

    // 5. Copia assets estáticos
    await this._copyAssets();

    // 6. Gera service worker (PWA)
    if (this.config.pwa?.enabled) await this._generateSW();

    // 7. Gera relatório
    const duration = Date.now() - start;
    Logger.info(`✅ Build concluído em ${duration}ms`);
    Logger.info(`📦 Saída: ${this.config.outDir}`);
  }

  async deploy(target = 's3') {
    const deployers = {
      s3: new S3Deployer(),
      vercel: new VercelDeployer(),
      netlify: new NetlifyDeployer(),
      custom: new CustomDeployer()
    };

    const deployer = deployers[target];
    if (!deployer) throw new Error(`Target '${target}' não suportado`);

    Logger.info(`📤 Deploy para ${target}...`);
    await deployer.deploy(this.config.outDir, this.config);
    Logger.info('✅ Deploy concluído');
  }

  async analyze() {
    // Gera relatório de análise de bundle
    Logger.info('📊 Gerando análise de bundle...');
    const stats = await this._getBundleStats();
    this._generateReport(stats);
  }

  async serve(port = 3000) {
    // Servidor de preview do build
    const handler = serveStatic(this.config.outDir);
    http.createServer((req, res) => handler(req, res, () => {
      res.statusCode = 404;
      res.end('Not Found');
    })).listen(port);
    Logger.info(`🌐 Preview em http://localhost:${port}`);
  }
}

// Deployer interface
class S3Deployer {
  async deploy(localDir, config) {
    const { S3Client, PutObjectCommand } = await import('@aws-sdk/client-s3');
    const client = new S3Client({ region: config.aws?.region || 'us-east-1' });
    const files = await fs.readdir(localDir, { recursive: true });
    for (const file of files) {
      const content = await fs.readFile(path.join(localDir, file));
      await client.send(new PutObjectCommand({
        Bucket: config.aws?.bucket,
        Key: file,
        Body: content,
        ContentType: this._mimeType(file)
      }));
    }
  }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |

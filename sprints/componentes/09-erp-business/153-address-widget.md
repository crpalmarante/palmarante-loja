# FiscalUI Framework

## Documento 153 — Address Widget

**Nível 9 — ERP Business Components**

**Versão 1.0**

Widget de endereço com busca por CEP, campos de endereço brasileiro e integração com formulários.

---

```html
<div class="ui-address-widget">
    <div class="ui-address-widget__cep-row">
        <div class="ui-field ui-field--sm">
            <label class="ui-field__label">CEP</label>
            <div class="ui-field__input-group">
                <input class="ui-field__input ui-mask-cep" placeholder="00000-000">
                <button class="ui-btn ui-btn--ghost ui-btn--sm" data-action="search-cep">
                    <span class="ui-icon ui-icon--search"></span>
                </button>
            </div>
        </div>
    </div>

    <div class="ui-address-widget__grid">
        <div class="ui-field ui-field--lg">
            <label class="ui-field__label">Logradouro</label>
            <input class="ui-field__input" placeholder="Rua, Avenida, ...">
        </div>
        <div class="ui-field ui-field--sm">
            <label class="ui-field__label">Número</label>
            <input class="ui-field__input" placeholder="Nº">
        </div>
    </div>

    <div class="ui-address-widget__grid">
        <div class="ui-field ui-field--md">
            <label class="ui-field__label">Bairro</label>
            <input class="ui-field__input" placeholder="Bairro">
        </div>
        <div class="ui-field ui-field--md">
            <label class="ui-field__label">Cidade</label>
            <select class="ui-field__select">
                <option value="">Selecione a cidade</option>
            </select>
        </div>
        <div class="ui-field ui-field--xs">
            <label class="ui-field__label">UF</label>
            <select class="ui-field__select">
                <option value="">UF</option>
                <option value="AC">AC</option>
                <option value="AL">AL</option>
                <option value="AP">AP</option>
                <option value="AM">AM</option>
                <option value="BA">BA</option>
                <option value="CE">CE</option>
                <option value="DF">DF</option>
                <option value="ES">ES</option>
                <option value="GO">GO</option>
                <option value="MA">MA</option>
                <option value="MT">MT</option>
                <option value="MS">MS</option>
                <option value="MG">MG</option>
                <option value="PA">PA</option>
                <option value="PB">PB</option>
                <option value="PR">PR</option>
                <option value="PE">PE</option>
                <option value="PI">PI</option>
                <option value="RJ">RJ</option>
                <option value="RN">RN</option>
                <option value="RS">RS</option>
                <option value="RO">RO</option>
                <option value="RR">RR</option>
                <option value="SC">SC</option>
                <option value="SP">SP</option>
                <option value="SE">SE</option>
                <option value="TO">TO</option>
            </select>
        </div>
    </div>

    <div class="ui-address-widget__complement">
        <div class="ui-field">
            <label class="ui-field__label">Complemento</label>
            <input class="ui-field__input" placeholder="Apto, Bloco, ...">
        </div>
    </div>
</div>
```

```js
class AddressWidget {
    constructor(el) {
        this.el = el;
        this._init();
    }

    _init() {
        this.cepInput = this.el.querySelector('.ui-mask-cep');
        this.logradouro = this.el.querySelector('[placeholder*="Logradouro"]');
        this.bairro = this.el.querySelector('[placeholder="Bairro"]');
        this.cidade = this.el.querySelector('select:nth-of-type(1)');
        this.uf = this.el.querySelector('select:nth-of-type(2)');
        this.numero = this.el.querySelector('[placeholder*="Nº"]');

        this.el.querySelector('[data-action="search-cep"]')
            ?.addEventListener('click', () => this._buscarCEP());
    }

    async _buscarCEP() {
        const cep = this.cepInput.value.replace(/\D/g, '');
        if (cep.length !== 8) return;

        try {
            const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await res.json();
            if (data.erro) {
                this.el.dispatchEvent(new CustomEvent('address:error', { detail: 'CEP não encontrado' }));
                return;
            }
            this.logradouro.value = data.logradouro || '';
            this.bairro.value = data.bairro || '';
            this.cidade.value = data.localidade || '';
            this.uf.value = data.uf || '';
            this.numero.focus();
            this.el.dispatchEvent(new CustomEvent('address:loaded', { detail: data }));
        } catch {
            this.el.dispatchEvent(new CustomEvent('address:error', { detail: 'Erro ao buscar CEP' }));
        }
    }

    getValue() {
        return {
            cep: this.cepInput.value.replace(/\D/g, ''),
            logradouro: this.logradouro.value,
            numero: this.numero.value,
            bairro: this.bairro.value,
            cidade: this.cidade.value,
            uf: this.uf.value
        };
    }

    setValue(data) {
        this.cepInput.value = data.cep || '';
        this.logradouro.value = data.logradouro || '';
        this.numero.value = data.numero || '';
        this.bairro.value = data.bairro || '';
        this.cidade.value = data.cidade || '';
        this.uf.value = data.uf || '';
    }

    clear() { this.setValue({}); }
}
```

---

# Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-07-25 | FiscalUI Team | Versão inicial |

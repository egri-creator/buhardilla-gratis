# SISTEMA DE LEAD GENERATION — Aisla Solar / CAE 2026

## ¿QUÉ SOMOS?
Somos **captadores de leads** para Aisla Solar (y otras instaladoras). Ellos ponen la instalación, nosotros ponemos los clientes. Cobramos:
- **75€ por visita técnica** realizada (el instalador va a casa del cliente a medir)
- **200€ por cierre** (instalación completada)

## ¿CÓMO GENERAMOS LEADS?

### Pilar 1 — SEO Local (entran ellos solos)
**Qué es:** 98 páginas web, una por cada municipio donde opera Aisla Solar. Cada página está optimizada para que cuando alguien busque en Google "aislamiento buhardilla perdida gratis [su ciudad]", encuentre nuestra página.

**Cómo funciona:**
1. La página explica el programa CAE y que es gratis
2. El visitante rellena un formulario
3. Nos llega su nombre y teléfono a Telegram
4. Lo pasamos a Aisla Solar → ellos llaman → cobramos

**Leads/día:** 5-15 (crece con el tiempo, el SEO es acumulativo)
**Coste:** 0€ (las páginas se alojan en Cloudflare Pages gratis)
**Tiempo hasta resultados:** 1-3 meses (Google tarda en indexar)

---

### Pilar 2 — Catastro WFS + OVC (la ventaja real)
**Qué es:** Extraemos los datos del Catastro (API pública del gobierno) de todas las viviendas que cumplen los requisitos del CAE en los 98 municipios.

**Qué datos obtenemos de cada vivienda:**
- Dirección exacta
- Nombre del propietario
- Año de construcción  
- Superficie de la vivienda
- Valor catastral
- Si está en un edificio con otras viviendas también elegibles (cluster)

**¿Para qué usamos estos datos?**

| Uso | Legal | Cómo |
|-----|:-----:|------|
| Identificar edificios con 5+ viviendas elegibles | ✅ | Se lo vendemos a Aisla Solar como oportunidad B2B. Ellos contactan al **administrador de la finca** (relación comercial, lícito) |
| Saber qué calles/zonas tienen más viviendas elegibles | ✅ | Creamos contenido SEO extra para esas zonas |
| Tener una base de datos de "leads potenciales" | ✅ | Datos públicos. No contactamos directamente al propietario, pero podemos entregar el listado a Aisla Solar para que ellos gestionen el contacto |
| Detectar comunidades de vecinos con necesidad | ✅ | Edificio con 5+ propietarios que necesitan aislamiento → se lo ofrecemos al administrador (B2B, 100% legal) |

**¿Por qué es tan potente?**
Porque NO estamos adivinando quién puede necesitar aislamiento. **Sabemos con certeza** qué viviendas:
- Tienen más de 20 años (sin aislamiento)
- Tienen buhardilla no habitable (dato catastral)
- Están en zonas climáticas frías (mayor ahorro = mayor motivación)
- Pertenecen a edificios donde se puede hacer una obra comunitaria (más fácil para el instalador)

**Leads/día:** 15-30 parcelas identificadas por ejecución
**Coste:** 0€ (API pública sin autenticación)
**Frecuencia:** Cada 6h vía GitHub Actions

---

### Pilar 3 — Blog + Google Discover
**Qué es:** 15 artículos sobre CAE, ahorro energético, cómo saber si tu buhardilla es válida. Google descubre estos artículos y los muestra gratis en Google Discover (móviles) y Google News.

**Leads/día:** 3-8 (tráfico informacional)
**Coste:** 0€

---

### Pilar 4 — Administradores de Fincas (B2B)
**Qué es:** Buscamos administradores de fincas en Google Maps en cada municipio. Les enviamos un email automático explicando que podemos ayudar a sus comunidades a aislar gratis.

**Por qué funciona:** Un administrador gestiona 10-30 comunidades. Si una comunidad tiene 5 vecinos que necesitan aislamiento, son 5 visitas × 75€ = 375€ solo por las visitas.

**Leads/día (B2B):** 5-15 administradores identificados
**Coste:** 0€ (Google Places API está dentro del crédito gratuito de $200/mes)

---

### Pilar 5 — Idealista Alertas
**Qué es:** Monitorizamos alertas de Idealista de áticos/buhardillas en venta. Si alguien vende una casa con buhardilla, probablemente también quiera aislarla antes de vender (o el comprador querrá hacerlo).

**Leads/día:** 3-6
**Coste:** 0€ (Gmail API)

---

## ¿CUÁNTOS LEADS/DÍA SON REALISTAS?

| Fuente | Leads/día | Tipo |
|--------|:---------:|:----:|
| Catastro (parcelas identificadas) | 15-30 | Datos de viviendas elegibles |
| SEO local (formularios) | 5-15 | Leads directos (la gente contacta) |
| Admin Fincas B2B | 5-15 | Leads comerciales |
| Blog Discover | 3-8 | Tráfico web |
| Idealista | 3-6 | Alertas de venta |
| **TOTAL** | **31-74** | **~50/día de media** |

De esos 50 leads/día:
- ~65% pasan el scoring mínimo (32/día)
- ~90% se entregan a Aisla Solar (29/día)
- ~70% los aceptan (20/día)
- ~17% se convierten en visita (3-4 visitas/día)
- ~30% de visitas → cierre (1 instalación/día)

## ¿CUÁNTO GANAS?

| Concepto | Diario | Mensual (22 días) |
|----------|:------:|:-----------------:|
| Visitas (3-4 × 75€) | 225-300€ | **4.950-6.600€** |
| Cierres (1 × 200€) | 200€ | **4.400€** |
| **TOTAL** | **425-500€** | **9.350-11.000€****

*En el primer mes, el SEO aún no genera. Restar 1.500-3.000€ del total.*

## ¿CUÁNTO CUESTA?

**0€/mes.** Todo corre en:
- GitHub Actions (gratis, 2.000 min/mes)
- Cloudflare Pages (gratis)
- Google Cloud (crédito gratuito $200/mes)
- Catastro API (pública, sin auth)
- Groq API (1M tokens/día gratis)

## ¿QUÉ TIENES QUE HACER TÚ?

**NADA.** Literalmente:
1. Configurar las API keys una vez (1 hora)
2. Subir a GitHub
3. Los leads llegan solos a tu Telegram

Cuando Aisla Solar te pague, solo tienes que:
- Facturarles (si eres autónomo/empresa)
- O si eres empleado, que te paguen nómina + comisiones

## ¿POR QUÉ ES MEJOR QUE CUALQUIER OTRO SISTEMA?

1. **No compites con nadie** — Nadie más usa el Catastro para esto
2. **No pagas por lead** — Todo es tráfico orgánico + datos públicos
3. **Escala solo** — Más tiempo = más SEO = más leads sin hacer nada
4. **B2B built-in** — Los clusters de edificios dan leads de varios vecinos a la vez
5. **Legal** — Catastro es público, SEO es contenido, B2B es relación comercial

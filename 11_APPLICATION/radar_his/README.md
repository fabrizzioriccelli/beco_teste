# Radar HIS São Paulo

Relatório de imóveis HIS/HMP na capital, montado só com dados oficiais:

| Fonte | O que traz | Atualização |
|---|---|---|
| GeoSampa, camada "HIS e HMP – Alvará de Execução" (WFS `geoportal:habitacao_popular`) | Alvarás HIS-1, HIS-2 e HMP desde ago/2019: endereço, SQL, unidades por categoria | Irregular (última: 13/09/2026) |
| Secretaria da Fazenda, "Guias de ITBI pagas" | Vendas desde 2006: valor, data, unidade, cartório e matrícula. **Sem nome de comprador ou vendedor** | Mensal |
| Banco Central (SGS 433 e 4391) | IPCA e CDI mensais | Mensal |
| Decretos 64.244/2025 e 64.895/2026 (texto oficial) | Tetos de preço de venda por categoria | Anual (janeiro) |

## Como rodar

```bash
pip install python-calamine shapely
python3 coletar.py --dados _dados        # baixa as fontes (~550 MB de ITBI na primeira vez)
python3 processar.py --dados _dados      # gera site/dados/*.json (~1 min)
cd site && python3 -m http.server        # abre o relatório em http://localhost:8000
```

A rede precisa permitir: `wms.geosampa.prefeitura.sp.gov.br`, `prefeitura.sp.gov.br`, `drive.prefeitura.sp.gov.br` e `api.bcb.gov.br`.

## Como a ligação alvará → venda funciona

1. Cada lote com alvará HIS/HMP gera chaves: setor e quadra fiscal (6 primeiros dígitos do SQL) + CEP + número.
2. Cada guia de ITBI com a mesma chave é ligada ao prédio.
3. A guia vira **unidade** quando o complemento indica apartamento ou torre. Vira **lote/terreno** quando não indica, ou quando o valor passa de R$ 2 milhões.
4. Guias da mesma unidade em até 90 dias contam como um único negócio. Guias com menos de 30% do valor típico do prédio são tratadas como complementares e ficam de fora.
5. A primeira compra e venda é a "1ª venda" e as seguintes são "revendas". Dação em pagamento e permuta ficam separadas.
6. "Acima do teto" só é marcado em prédios 100% HIS/HMP, para compra e venda a partir de 28/05/2025.

## Limitações

- Não há nome nem telefone de proprietários nos dados abertos.
- A camada da Prefeitura começa em 2019. HIS mais antigas não aparecem no mapa, mas a calculadora aceita qualquer data.
- O valor do ITBI é o declarado pelo contribuinte.
- Unidades com complemento escrito de formas diferentes ao longo do tempo podem não ser reconhecidas como a mesma, o que subestima revendas.

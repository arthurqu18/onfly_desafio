## Primeiro teste: `test_currency.py`

```text
E       AssertionError: assert '118.45' == '642.00'
E         
E         - 642.00
E         + 118.45
```

- **Causa:** a função `convert_to_brl` contém um erro em:
  ```python
  return Decimal(str(float(amount) / float(rate)))
  ```
- **Como investiguei:** após compreender o código e ler as regras de negócio (que pedia `*` ao inves de `/`), percebi o erro.
- **Correção:**
  ```python
  return Decimal(str(float(amount) * float(rate)))
  ```
- **Resultado:** `tests/test_currency.py::test_currency_conversion_to_brl PASSED`

---

## Segundo teste: `test_nights.py`

```text
>       assert report["summary"]["total_room_nights"] == 3
E       assert -28 == 3

tests/test_nights.py:19: AssertionError
```

- **Causa:** a função `calculate_room_nights` contém um erro no calculo de noites:
  ```python
  return (checkout.day - checkin.day) * rooms
  ```
- **Como investiguei:** observei a função em questão e com ajuda das regras de negócio percebi que o calculo de noites estava incorreto, ao contar somente o dia, na virada de mês, essa conta pode ficar negativa. Então, faz-se a conta considerando a data por completo e pegando a quantidade de dias ocorridos.
- **Correção:**
  ```python
  return (checkout - checkin).days * rooms
  ```
- **Resultado:** `tests/test_nights.py::test_nights_across_month_boundary PASSED`

---

## Terceiro teste: `test_regression_report.py`

Não houve erros na execução deste teste: `tests/test_regression_report.py::test_regression_report_on_sample PASSED`

- **Investigando:** olhando e fazendo as contas manualmente, os `asserts` estão escritos corretamente e o resultado deste CLI, que contém somente reservas confirmadas e canceladas, saiu como esperado.

---

## Quarto teste: `test_status_rules.py`

```text
        assert report["summary"]["total_reservations"] == 3
        assert report["summary"]["confirmed_reservations"] == 1
        assert report["summary"]["cancelled_reservations"] == 1
        assert report["summary"]["no_show_reservations"] == 1
>       assert report["summary"]["total_amount_brl"] == "100.00"
E       AssertionError: assert '120.00' == '100.00'
E         
E         - 100.00
E         ?  ^
E         + 120.00
E         ?  ^

tests/test_status_rules.py:20: AssertionError
```

- **Causa:** a função `is_billable` possui um erro de lógica em `return status != "CANCELLED"`, pois considera somente `"CANCELLED"` como não contável nos totais financeiros.
- **Como investiguei:** após leitura e entendimento do código, percebi que `is_billable` contém esse erro de lógica, causando um erro no cálculo do montante total. Para a correção, tem que considerar `"NO_SHOW"` como não contável também.
- **Correção:**
  ```python
  return status != "CANCELLED" and status != "NO_SHOW"
  ```
- **Resultado:** `tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show PASSED`

---

## Quinto Teste: `test_top_hotels.py`

```text
>       assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02", "H03"]
E       AssertionError: assert ['H04', 'H03', 'H02'] == ['H01', 'H02', 'H03']
E         
E         At index 0 diff: 'H04' != 'H01'
E         Use -v to get more diff

tests/test_top_hotels.py:18: AssertionError
```

- **Causa:** na função `build` da classe `ReportBuilder` há um erro na ordenação dos tops hoteis, que deveria ordernar decrescentemente os hoteis com base no montante total:
  ```python
  ranked_hotels = sorted(hotels.items(), key=lambda item: (item[1]["amount"], item[0]))
  ```
  ordena crescentemente.
- **Como investiguei:** olhando e interpretando o código e lendo as regras de negócio, percebi o erro de lógico dentro dessa classe. Para correção, basta ordenar reversamente (decrescentemente).
- **Correção:**
  ```python
  ranked_hotels = sorted(hotels.items(), key=lambda item: (item[1]["amount"], item[0]), reverse=True)
  ```
  ou
  ```python
  ranked_hotels = sorted(hotels.items(), key=lambda item: (item[1]["amount"], item[0]))[::-1]
  ```
- **Resultado:** `tests/test_top_hotels.py::test_top_hotels_are_ranked_descending PASSED`

---

## Conclusão

Todos os 5 testes passaram:

```text
tests/test_currency.py::test_currency_conversion_to_brl PASSED                                                   [ 20%]
tests/test_nights.py::test_nights_across_month_boundary PASSED                                                   [ 40%]
tests/test_regression_report.py::test_regression_report_on_sample PASSED                                         [ 60%]
tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show PASSED                               [ 80%]
tests/test_top_hotels.py::test_top_hotels_are_ranked_descending PASSED                                           [100%]
```

Foram gerados corretamente o `output/exemplo.json` e o `output/report.json`.

Foi rodado o `pytest-cov` para ver a cobertura do projeto, que deu como cobertura `0%`, ocorreu isso por causa das decisões de projeto do desafio (conversei com o copilot sobre isso, como consta no relatório de uso de IA). A partir da cobertura, iria ver quais classes, funções precisariam de mais testes, mas para não mudar a semântica do projeto, decidi não me embasar na cobertura de testes.

Gerei alguns testes extras para o projeto, com auxilio da IA, para melhorar a qualidade do sistema.
A função `build_report` foi adiciona em `helpers.py` para garantir boas práticas na criação e uso de testes, como no uso de APIs públicas.

- `test_room_nights_and_average_include_all_rooms`: testa o sistema ao fazer uma reserva com mais de 1 quarto reservado; os 5 primeiros testes testavam somente com 1 quarto alugado.
- `test_top_hotels_respect_requested_limit`: testa se o sistema retorna corretamente a quantidade de hotéis definidos a priori.
- `test_invalid_reservation_input.py`: assegura que não há nenhuma reserva com alguma data inválida.
- `test_report_uses_supplied_generation_time`: verifica se a data fornecida à função `build_report` retorna no formato ISO esperado.
- `test_empty_report.py`: garante que ao receber um arquivo com nenhum dado, o retorno também será tudo zerado e coleções vazias.

Conjuntamente, todos os testes passaram: `10 passed in 0.76s`
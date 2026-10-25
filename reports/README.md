# Қазақ тіліндегі есептер

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

Оқу жылы: 2025-2026.

**14 зертханалық есеп — 212 бет. Қорытынды есеп — 8 бет. Барлығы 15 PDF, 220 бет.**

[Барлық есепті архивпен жүктеу](devops-reports-kk.zip) · [Бастапқы файлдар](source/README.md) · [Техникалық тексеру](quality-check.json).

| № | Тақырып | PDF | Бастапқы файл |
|---|---|---|---|

| 1.1 | Тапсырмалар сервисінің API интерфейсі | [PDF · 13 бет](lab01-part1-report.pdf) | [JSON](source/lab01-part1-report.json) |

| 1.2 | Сұрауды талдау және жоба статистикасы | [PDF · 19 бет](lab01-part2-report.pdf) | [JSON](source/lab01-part2-report.json) |

| 2.1 | Dockerfile және құрастыру кэші | [PDF · 12 бет](lab02-part1-report.pdf) | [JSON](source/lab02-part1-report.json) |

| 3.1-3.2 | Сервиске арналған PostgreSQL | [PDF · 15 бет](lab03-postgres-report.pdf) | [JSON](source/lab03-postgres-report.json) |

| 3.3 | Docker Compose және деректердің өмірлік циклі | [PDF · 14 бет](lab03-compose-report.pdf) | [JSON](source/lab03-compose-report.json) |

| 4.1 | Git және GitHub-та бірлескен жұмыс | [PDF · 15 бет](lab04-git-report.pdf) | [JSON](source/lab04-git-report.json) |

| 4.2 | GitHub ережелері және шығарылым | [PDF · 17 бет](lab04-release-report.pdf) | [JSON](source/lab04-release-report.json) |

| 5.1 | GitHub Actions арқылы үздіксіз интеграция | [PDF · 14 бет](lab05-ci-report.pdf) | [JSON](source/lab05-ci-report.json) |

| 5.2 | Үздіксіз жеткізу және кері қайтару | [PDF · 14 бет](lab05-cd-report.pdf) | [JSON](source/lab05-cd-report.json) |

| 6.1 | Қолданба ақаулары және қайта іске қосу | [PDF · 13 бет](lab06-failures-report.pdf) | [JSON](source/lab06-failures-report.json) |

| 6.2 | Ресурстар, тәуелділік және диагностика | [PDF · 15 бет](lab06-resources-report.pdf) | [JSON](source/lab06-resources-report.json) |

| 7.1 | Метрикалар және PromQL | [PDF · 17 бет](lab07-metrics-report.pdf) | [JSON](source/lab07-metrics-report.json) |

| 7.2 | Grafana панельдері және алерттер | [PDF · 17 бет](lab07-alerts-report.pdf) | [JSON](source/lab07-alerts-report.json) |

| 8 | Инцидентті анықтау және қалпына келтіру | [PDF · 17 бет](lab08-incident-report.pdf) | [JSON](source/lab08-incident-report.json) |

| Қосымша | Жұмыстардың қорытынды нәтижелері | [PDF · 8 бет](submission-summary-kk.pdf) | [JSON](source/submission-summary-kk.json) |

## Өңдеу

```powershell
python scripts/build_reports.py
python scripts/check_reports.py
```

Мәтін reports/source ішіндегі JSON файлдарында өңделеді. Бастапқы код, HTTP жауаптары және суреттер жеке техникалық материалдармен байланысты.

[Негізгі бет](../README.md) · [Рәсімдеу параметрлері](../docs/FORMATTING_STANDARDS.md).

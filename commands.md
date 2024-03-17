```bash
cd tools/database-dev
```

```bash
docker compose up -d
```

```bash
docker run --rm --network="fintech-network" -v D:/hse/pr/python_sem/hw_repos/hse-fault-tolerant-systems-python-2023-fintech-lyakhliliana/product_engine/migrations:/app liquibase/liquibase:4.19.0 --defaultsFile=/app/dev.properties update
```

```bash
docker run --rm --network="fintech-network" -v D:/hse/pr/python_sem/hw_repos/hse-fault-tolerant-systems-python-2023-fintech-lyakhliliana/origination/migrations:/app liquibase/liquibase:4.19.0 --defaultsFile=/app/dev.properties update
```

```bash
cd ../../
```

```bash
docker compose up -d
```

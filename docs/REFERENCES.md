# Reference documentation (consult at implementation time)

1. OpenAI Codex skills discovery, `.agents/skills`: https://learn.chatgpt.com/docs/build-skills
2. Debezium PostgreSQL connector, snapshots / LSN / logical replication: https://debezium.io/documentation/reference/stable/connectors/postgresql.html
3. Apache Flink fault tolerance & end-to-end source/sink conditions: https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/
4. Flink checkpointing: https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/
5. OpenRouter per-generation metadata (requires a generation ID): https://openrouter.ai/docs/api/api-reference/generations/get-generation
6. dbt official docs home for model contracts, tests, snapshots: https://docs.getdbt.com/docs/build/data-tests
7. PostgreSQL logical replication docs: https://www.postgresql.org/docs/current/logical-replication.html

These are technical source references, not product endorsements or proof of successful implementation. Reconfirm versions and actual API behavior at each implementation phase; do not rely on docs alone for end-to-end guarantees.

from pytest_postgresql import factories

postgresql_proc = factories.postgresql_proc()
postgresql = factories.postgresql("postgresql_proc")

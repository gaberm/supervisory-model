import pytest
from state_memory.schema_manager import SchemaManager
from state_memory.state_memory import StateMemory
from _records import Vehicle, RUN_ID


@pytest.fixture
def state_memory(postgresql):
    SchemaManager(postgresql, RUN_ID).setup([Vehicle])
    info = postgresql.info
    dsn = f"host={info.host} port={info.port} user={info.user} dbname={info.dbname}"
    sm = StateMemory(dsn, RUN_ID)
    yield sm
    sm.close_conn()


def test_insert_outputs(state_memory, postgresql):
    state_memory.insert_outputs(
        Vehicle,
        [
            {"veh_id": "veh_1", "soc": 0.5, "time": 1.0},
            {"veh_id": "veh_2", "soc": 0.8, "time": 2.0},
        ],
    )
    cur = postgresql.cursor()
    cur.execute(f"SELECT veh_id, soc FROM {RUN_ID}.vehicle ORDER BY time")
    assert cur.fetchall() == [("veh_1", 0.5), ("veh_2", 0.8)]

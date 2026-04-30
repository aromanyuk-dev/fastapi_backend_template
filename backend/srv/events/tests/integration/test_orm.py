
from sqlalchemy import text
import pytest


@pytest.mark.asyncio
async def test_events_mapper_can_load_lines(session):
    async for s in session:
        await s.execute(
            text(
                """
                INSERT INTO events (id, title, description, start_time, end_time,
                                    age_limitations, max_quantity, author_id, created_at, updated_at)
                VALUES (1, 'Concert', 'Very interesting',
                        '2025-12-10 18:00:00', '2025-12-10 20:00:00',
                        18, 100, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
            )
        )



        result = await s.execute(text("SELECT * FROM events LIMIT 1"))
        row = result.first()
        assert row.id == 1
        assert row.title == 'Concert'



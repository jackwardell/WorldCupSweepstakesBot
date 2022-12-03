from src.crons.ingest_draw.__main__ import main as main_draw
from src.crons.ingest_fixture_events.__main__ import main as main_fixture_events
from src.crons.ingest_fixtures.__main__ import main as main_fixtures
from src.crons.ingest_participants.__main__ import main as main_participants
from src.crons.ingest_players.__main__ import main as main_players
from src.crons.ingest_sweepstake_categories.__main__ import main as main_sweepstakes_categories
from src.crons.ingest_teams.__main__ import main as main_teams

if __name__ == "__main__":
    main_teams()
    main_participants()
    main_draw()
    main_fixtures()
    main_sweepstakes_categories()
    main_players()
    main_fixture_events()

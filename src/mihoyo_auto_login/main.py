import typer
import yaml
import asyncio
from genshin import Client, Game
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, StringConstraints
from typing_extensions import Annotated

app = typer.Typer()


class User(BaseModel):
    uid: int = Field(..., gt=0, description="User ID must be a positive integer")
    token: Annotated[
        str,
        StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z0-9_.]+$"),
    ] = Field(..., description="Token must be obtained from hoyoverse")
    games: Optional[List[Game]] = None


async def claim_reward(user: User, game: Game):
    client = Client()
    client.set_cookies({"ltuid_v2": user.uid, "ltoken_v2": user.token})
    await client.claim_daily_reward(game=game)


@app.command()
def claim_rewards(yaml_file: str, game: Optional[Game] = None):
    try:
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file)

        users  = [User(**user) for user in data["users"]]

        if not users:
            typer.echo("No users specified.")
            raise typer.Exit(1)

        asyncio.run(process_users(users, game))
    except ValidationError as e:
        typer.echo(f"Error in user data: {e}")


async def process_users(users: List[User], default_game: Optional[Game]):
    tasks = []
    for user in users:
        games = user.games if user.games else [default_game] if default_game else [Game.GENSHIN]
        for game in games:
            tasks.append(claim_reward(user, game))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    app()

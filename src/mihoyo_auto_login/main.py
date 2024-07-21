import typer
import yaml
import asyncio
from genshin import Client, Game
from typing import List
from pydantic import BaseModel, Field, ValidationError, StringConstraints
from typing_extensions import Annotated

app = typer.Typer()


class User(BaseModel):
    uid: int = Field(..., gt=0, description="User ID must be a positive integer")
    token: Annotated[
        str,
        StringConstraints(strip_whitespace=True, pattern=r"^[a-zA-Z0-9]{8,}$"),
    ] = Field(..., description="Token must be obtained from hoyoverse")


async def claim_reward(user: User, game: Game):
    client = Client()
    client.set_cookies({"ltuid": user.uid, "ltoken": user.token})
    await client.claim_daily_reward(game=game)


@app.command()
def claim_rewards(yaml_file: str, game: Game):
    try:
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file)

        users: List[User] = [User(**user) for user in data["users"]]

        asyncio.run(process_users(users, game))
    except ValidationError as e:
        typer.echo(f"Error in user data: {e}")


async def process_users(users: List[User], game: Game):
    tasks = [claim_reward(user, game) for user in users]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    app()

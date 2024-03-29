<div align="center">
 <h1>
     sheepcord
 </h1>
 
 <img src="https://img.shields.io/github/issues/keenanoh/sheepcord">
 <img src="https://img.shields.io/github/forks/keenanoh/sheepcord">
 <img src="https://img.shields.io/github/stars/keenanoh/sheepcord">
 <img src="https://img.shields.io/github/license/keenanoh/sheepcord">
 <img src="https://tokei.rs/b1/github/keenanoh/sheepcord">
 
 <br>
 <br>
 
 A Discord interactions library built with blacksheep and pydantic.
 
</div>

## Features
- [x] Discord HTTP Interactions Server
- [x] Dependency Injection


## Examples
main.py
```py
import sheepcord

bot = sheepcord.Bot(
    "TOKEN",
    "APPLICATION ID",
    "SECRET",
)
bot.load_module("module")
bot.start()

```
module.py
```py
import sheepcord


@sheepcord.command("hello", "says hello")
@sheepcord.option(sheepcord.OptionType.USER, "user", "the user")
async def hello(_: sheepcord.Interaction, user: sheepcord.User, bot: sheepcord.Inject[sheepcord.Bot]) -> sheepcord.InteractionResponse:
    return sheepcord.InteractionResponse(
        type=sheepcord.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=sheepcord.Message(content=f"Hello, {user.mention}!")
    )


loader = sheepcord.Loader(locals())
```

## Contributing
All contributions are welcome. Please format the code with [black](https://github.com/psf/black).

## Attention
Sheepcord is still in development and is not ready for production.


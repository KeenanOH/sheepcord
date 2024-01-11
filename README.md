<div align="center">
 <h1>
   <a href="https://shinobou.github.io/sheepcord">
     sheepcord
   </a>
 </h1>
 
 <img src="https://img.shields.io/github/issues/Shinobou/sheepcord">
 <img src="https://img.shields.io/github/forks/Shinobou/sheepcord">
 <img src="https://img.shields.io/github/stars/Shinobou/sheepcord">
 <img src="https://img.shields.io/github/license/Shinobou/sheepcord">
 <img src="https://tokei.rs/b1/github/Shinobou/sheepcord">
 
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


## Documentation
https://keenanoh.github.io/sheepcord

## Contributing
All contributions are welcome. Please format the code with [black](https://github.com/psf/black).

## Attention
Sheepcord is still in development and is not ready for production.


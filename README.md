# sheepcord
![](https://img.shields.io/github/issues/Shinobou/sheepcord)
![](https://img.shields.io/github/forks/Shinobou/sheepcord)
![](https://img.shields.io/github/stars/Shinobou/sheepcord)
![](https://img.shields.io/github/license/Shinobou/sheepcord)

A Discord interactions library built with blacksheep and pydantic.


## Examples
```py
import sheepcord


@sheepcord.command("hello", "says hello")
@sheepcord.option(sheepcord.OptionType.USER, "user", "the user")
async def hello(_: sheepcord.Interaction, user: sheepcord.User):
    return sheepcord.InteractionResponse(
        type=sheepcord.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=sheepcord.Message(content=f"Hello, {user.mention}!")
    )


loader = sheepcord.Loader(locals())
```


## Documentation
https://shinobou.github.io/sheepcord

## Contributing
All contributions are welcome. Please format the code with [black](https://github.com/psf/black).

## Attention
Sheepcord is still in development and is not ready for production.


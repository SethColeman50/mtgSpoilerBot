# mtgSpoilerBot

A discord bot to post new spoiler cards for Magic: the Gathering by scrapping https://www.magicspoiler.com/. Currently only avaliable to self host.

## Developer setup
### Prerequites
Please make sure you have the following prerequisites:
- [python](https://www.python.org/downloads/) 3.13 or above
- [Docker](https://docs.docker.com/engine/install/) and Docker compose
- [SQLite](https://sqlite.org/index.html) (should be installed on most machines)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Downloading the source code
Clone the repository:
```bash
git clone https://github.com/SethColeman50/mtgSpoilerBot.git
cd mtgSpoilerBot
```

### Creating a discord bot
A tutorial is linked [here](https://discordpy.readthedocs.io/en/stable/discord.html).

#### Bot Premissions
Needed premissions:
- View Channels (for setting the spoiler channel)
- Send Messages
- Embed Links 
- Attach Files (for sending the images)

### Creating the local files
Create a file named `.env` in the root directory with these contents:
```
TOKEN=<bot token from discord>
```
(Any text enclosed in angle brackets (`<>`) is to be fully replaced)

### Building
This project is built with Docker Compose:
```bash
docker compose up
```
and can be brought down with:
```bash
docker compose down
```
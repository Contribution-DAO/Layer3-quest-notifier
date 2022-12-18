# Layer3 Quest Notifier
This is a contribution work for Layer 3 team. I created this bot becuase I want to get an `Early Birds` achievement.

## Deployment Bot URL
The announcement channel can be found [here]()

(Yes, it's doesn't redirect you to the bot. I'll need to test it first)

## Usage
Skip this part if you don't want to host this bot on your personal machine

### 1. Get the telegram tokens
1. Create a telegram channel and a bot. The bot can be created using the `@botfather` account
2. Copy your bot's token to the `.env` file, and put it to the `TELEGRAM_TOKEN` variable. See tha example on `.env.example`
3. Add your bot as an admin to the created telegram channel
4. Make your telegram channel public, and add it's url. The added url will be the ID used in the `.env` file.

### 2. Spinning up the service
Run a script using the following command:
```bash
./scripts/build_docker.sh  # build a docker container
./scripts/run_docker.sh  # start a docker container
```
**Make sure you installed docker first!**

## Contribution
Fork this repository and opening a pull request

## Author
`chompk.eth`
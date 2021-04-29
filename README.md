# VirtualHuman

If you would like to talk to this agent, you can directly use this link http://34.219.250.232/guest/conversations/production/c6050488ccce4680a3fce7adc7ed69a5 as a evaluator.

Or you can clone this repository and start it on your local server.

First install the dependecies by 

```shell
pip3 install -r requirements
```

Then go to directory [Noah](Noah), that's where we store the agent.

Then, Brian Rasa NLU and Rasa Core by

```shell
rasa train
```

Before you start the conversation, you should start rasa action server by 

```shell
rasa run actions
```

And then talk to the agent in your terminal by running:

```
rasa shell
```

If you would like to use the voice bot,

Start the rasa server by

```
rasa run
```

And then execute

```shell
python3 voice_bot.py
```


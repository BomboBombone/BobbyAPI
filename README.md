# BobbyAPI
Chat AI APIs for [DiskoAIO](https://github.com/BomboBombone/DiskoAIO) 

## How it works
It uses a slightly modified version of Chatterbot (modified to allow for more efficience, larger databases and multi "botting".
The API can be used very easily to collect info and train Bobby (the bot).

## Does it have collective knowledge of every chat?
No, Bobby will start from scratch everytime it enters a new server, but every instance of Bobby (even though there is only one instance on the server, more clients can use it) will share knowledge of each server. So if client 1 uses Bobby on server A then when client 2 uses Bobby on the same server it will use the already learnt knowledge to chat.

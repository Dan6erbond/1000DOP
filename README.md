# MetroBot (a.k.a. 1000DOP Bot)
Created by [Dan6erbond](https://github.com/Dan6erbond)

MetroBot was originally created for [/r/1000daysofpractice](https://www.reddit.com/r/1000daysofpractice/) on Reddit. As a crucial member of the subreddit, it works to maintain the flair-counting system that helps subreddit members keep track of the total amount of days they have logged in the daily threads. This allows members to update their flairs only when they log in the daily threads, allowing them to skip a day as needed without having to reset their flair.

## Features
* Assigns requested flairs to users.
* Updates flairs when prompted by a user-command (in the daily threads).
* Sends a customizable reply to users who have not formatted their logs correctly.

## Usage
### Installation

* Invite MetroBot to your subreddit!
* Hosting
**[yeah I have no idea..]**

### How does it work?

#### Requesting a New Flair
Users who have not started logging can request a flair from MetroBot with these instructions.

1. Users can request a flair by mailing MetroBot on Reddit (via private message).Example [link] The message should be formatted like so:
[emoji]
**include screenshot**

  * Up to 4 emojis may be requested due to Reddit's word-count restriction on user flairs.
  * An emoji with no number indicates a starting point of `[emoji] 0 day(s)`.
  
2. MetroBot will then assign the user a flair, like so:

[image]

#### Requesting a Modified Flair
Users who have already started logging, or want to modify their flair (such as adding or deleting emojis) should:

1. PM MetroBot with this modified message:
[emoji][number]

  * In order to prevent abuse of the system, MetroBot will scan through all daily threads to determine the highest number it can assign to the user. This number is equal to or lower than the number of correctly formatted logs by the user. As an example, if the user logged for 3 days and requested a flair with 4 days, MetroBot will **not** assign the flair. 

2. MetroBot will then assign a flair like so:

[image]

#### Logging in Daily Threads


### Screenshots

* **mod log?**
* what flair looks like
* example of templates

## FAQ/Troubleshooting

#### Can moderators still edit user flairs manually?
Yes. As long as the correct format of the flair is maintained, moderators can edit or correct user flairs and MetroBot will still recognize them. Moderator edits will override the minimal-log-# requirement.

#### Reddit or the bot went offline, how will MetroBot deal with backlogged activity?
[Technical Answer?] MetroBot can deal with backlogged activity and will update flairs accordingly when it is back online. Moderators should not attempt to fix flairs at this time until the bot is fully operational, as it will add onto edited flairs.

## Contributing

**copied from Banhammer.py**

The 1000DOP Bot is open-source! That means we'd love to see your contributions and hopefully be able to accept them in the next release. If you want to become a contributor, try to follow these rules to keep the code clean:

1. Variable and file names must be written in snake-case. (eg. variable_name)
2. Class names must be pascal-case. (eg. ClassName)
3. Only use async where necessary.
4. Use the OOP approach; create classes when it makes sense.
5. Document as much as you can, preferably with inline comments.
6. Use the Google Style docstring format.
7. Store data in JSON, INI or YAML format to eliminate dependencies for other formats.
8. Create an __init__.py file for sub-modules.

## Links
[your site]
See MetroBot in action at [r/1000daysofpractice].


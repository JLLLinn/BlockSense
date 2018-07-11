# BlockSense
### Install Mongo to Store Tweets
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
$ cat /var/log/mongodb/mongod.log
```
### Install Necessary Library
http://api.mongodb.com/python/current/
``` 
$ python3 -m pip install pymongo 
```
```
$ pip3 install pytz
```
```
$ pip3 install tweepy
```
### Create a database named "twitterdb" for storing tweets


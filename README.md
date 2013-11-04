simpleRaft
==========
[![Build Status](https://travis-ci.org/streed/simpleRaft.png?branch=master)](https://travis-ci.org/streed/simpleRaft)

What?
=====
A implementation of Raft in pure Python. 

Why?
====
After reading a few papers on the Raft algorithm I figured I would implement it and use it for projects of mine that require the 
consistency that Raft provides to ensure their correctness.

Details
=======

This implementation tries to stay as pure Python as possible to ensure that as few dependencies are required to run this outside of the code in this repo.
I am also striving to have it run on Python 2.6+ as well to make it as flexible as possible. 

The system is designed in two parts. There are a system of state classes that define the functionality required for the specific states that a node can
go through during the running of Raft, these include:

* Follower
* Candidate
* Leader

Each one has their roles defined in their class files. Along with these state classes there are defined messages that will be used to keep the 
message format well defined and abstracted from the wire format as much as possible. 

The final part is the communication layer. The current communication layer will use Gossiping using randomized subgroups at the moment, but it will
be written in such a way so as to be easy to implement and plug in a different communicationl layer at a later time.

References:
==========
* [In Search of an Understandable Consensus Algorithm](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [Raft Lecture](http://www.youtube.com/watch?v=YbZ3zDzDnrw)

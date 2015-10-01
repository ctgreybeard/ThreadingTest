# Threading Playtime

The purpose of these modules is simply a playground for me to learn about
Python Threads, Queues, Scheduling, interprocess communication
and related "things" ...

This is written against Python 3.4 initially but may be up/downgraded as necessary.
My initial target is a Raspberry Pi and, at the time of this writing has only Python 3.2
available but Jessie is out and may have a later version of Python available.
I'm writing this on a Mac and could use 3.5 but will hold back a bit.

## The "Plan" ...

I am using this to learn the intricasies of Python Threading. In deciding to do it
I also thought it might be a good tutorial for someone else.  So that's what this is
supposed to be.

The plan is to build the project from simple to functional, if marginally so, using *git*
to mark instructional progress. I'll be using *tags* to mark the spots where I think the
important parts are and will be referring to them here.

Using *git* you should be able to roll the project back to a spot and follow the discussion
for that *tag*. The *git* diffs will also show the changes from one tag to the next.

I'm using the **dev** branch to make incremental testing changes.
The *tags* will be all against the **main** branch.

### git commands

Personally, I like the [Tower app](http://git-tower.com) on the Mac. But for this project
simple *git* commands will suffice.

Your most used *git* command will be

```
git checkout *tag*
```

where ** \*tag\* ** is the point you want the project to show.

Try **git checkout BeginHere** and look at the files that you see. The threadtest.py
source has *nothing* useful in it at all. but if you then do **git checkout master**
you are right back to where you started with everything in place.

Another very useful feature of using *git* is that you can make changes to the programs
in place, try out your changes, then revert back to the originals easily.

Or, conversely, if you want to SAVE your changes you can easily use git to do that so
you may return to them later.  I will put instructions later in this document for how to
do both of those things if you are interested.

So, let's continue with the **TAGS** that I have defined:

#### BeginHere

Use **git checkout BeginHere**

This point is the very beginning of the project. The main program, threadtest.py, is
a simple shell set up to run as the __ \_\_main\_\_ __ program. The threading module is imported
(but is only used as a superclass for ThreadTest), the main class is defined as a
useless stub, and the logic to use for intialization is started. You can run this and it
should simply print the message "Running in \_\_main\_\_".

The intent is to make ThreadTest run as a consumer of the "main" queue under its own thread.
It will pull "jobs" off the queue and execute arbitrary functions on request. It will continue
to do this until it is requested to stop. How we make that request will be developed as we go.

Right now it does none of this, let's try and fix that.

#### BasicPieces

This is a big change from before but it fleshes out the three main pieces of the project skeleton.

ThreadTest now has some real code. The two function definitions __ \_\_init\_\_ __ and run are required
when subclassing Thread. __ \_\_init\_\_ __ is simply calling the superclass' __ \_\_init\_\_ __ function to be
sure the real Thread capabilities are initialized properly. We'll cover the run() function
shortly.

A new class is introduced **Job**. This simple class simply holds a pointer to an arbitrary
function and its optional arguments. This Job object is what we are going to put into the queue
for the ThreadTest thread to process. In python functions can be used as any other object which
makes this sort of problem easy to do. We will use this simple structure to perform many things.

The global queue functions are described next. As I know we will be using more than one queue I went
and jumped the gun on implementing an arbitrary number of queues available. This isn't really
necessary for this project but it may prove useful. When a queue is requested by name it is searched
for uin the global queue dictionary, \_queuedict. If the named queue doesn't exist a FIFO queue of
that name is created. The pointer to the named queue is then returned.

The _dispatch_ functions simply create a Job object from the supplied parameters and put that onto the named
queue. This may be too restrictive and we may need to change that later but it's OK for now ...

Finally, the \_\_main\_\_ code defines a simple function to use as a Job, puts the job onto the **main**
queue, creates the ThreadTest object
that will perform the main queue consumer function, starts the thread then waits for it to complete.

Go ahead and run this by executing the **runit** script.  Use "./runit" in a terminal window.

Cool! Did it run? I hope so. If not then I have to leave it to you to make the changes needed to
get it to work on your system.

Assuming it runs OK is great but what makes it stop? Well, nothing yet, we'll work that one next.
In the mean time a couple of Ctrl-C's should kill it.

#### WeCanStop

Lets talk a bit about some useful *git* commands. As we move from one spot in this narrative to the next you
will want to see what the changes are.
I will refer to changes sometimes by line numbers and git can help you pinpoint the spots.

*git* can show you the changes between any two spots in the tree. We will use this to see what changes have
happened between two tags.

First, check out **WeCanStop**, you should know how to do that.

Then use the following command to see what the changes are:

```
git diff BasicPieces
```

What you should see are the *diffs* from the current code from **WeCanStop** and **BasicPieces** with a little context
from the enclosing unchanged lines.
Unfortunately, *git* doesn't know what's important to you and what isn't so you will see changes to any file that has changed.
Changes to the README aren't that interesting or the vim Session.vim file (not sure why that's included, I may just
set it to ingore.)
So try this:

```
git diff BasicPieces -- threadtest.py
```

That will limit the diff to just the code parts.

In case you aren't familiar with a diff, the code lines beginning with '+' are lines added, those with '-' have been removed.
So you can see what changes have occurred.

Look at the diff to go over the changes we have made.

We imported a new module, readline. This is strictly cosmetic. It allows line editing for the inout function we use below.

The first real change is what we do with the Job that we pull from the queue. We check first to see if it is not None.
We can't inspect or run it if it's None and if it's None -OR- the function within it is None then I call that a
Poison Pill and stop running the loop.
This will exit the thread and leave anything remaining in the queue in the queue.
But we are ending the jobs so that's OK for this program.

Further down in the \_\_main\_\_ section we have a loop reading from the terminal.
Because this is a contrived example you probably wouldn't really be doing this but imagine that it is some activity
that accepts user input and posts work to the main queue.
It has some way of recognizing a request to stop and so would post the poison pill at that time, wait for the thread to
stop (that's what main.join() does) and exit.

So go ahead an run this.
Enter a few nonesense lines then enter a null line and it should quit.
Maybe we should call this Parrot? as that's all it does.
Not terribly impressive but it is doing it in two Threads: the first is the system Main thread, that's what
the interpreter runs in and what is running the input() loop.
The second Thread we created and scheduled with main.start().
It doesn't look like it probably but these are independent.
When the Main system Thread blocks for the terminal I/O in input() the other thread is free to run.
We'll demonstrate that shortly.

But first I want to make a basic change to the design.
Do you see that the dispatch_queue routines create a Job internally?
And that this forces us to peek inside that Job in the main loop to see if the function is None?
I don't think this is good design; what we want is that the dispatch_queue function should accept ANY sort of object
and put it on the queue, and the consumer then can check to see if it's None or not and verify that it's the
correct sort of object.

But that also means we can use the same dispatch_queue routine to post other types of objects; like maybe data
objects rather than Job objects.
That might prove useful later on in the project.
Let's do that first ...

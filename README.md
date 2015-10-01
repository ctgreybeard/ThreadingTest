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

Go ahead and run this by executing the **runit** script.  Use "./runit" in a terminal window.

Cool! Did it run? I hope so. If not then I have to leave it to you to make the changes needed to
get it to work on your system.

Assuming it runs OK is great but what makes it stop? Well, nothing yet, we'll work that one next.
In the mean time a couple of Ctrl-C's should kill it.
that will perform the main queue consumer function, starts the thread then waits for it to complete.

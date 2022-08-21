# Arachnida

Web scrapping.

## Spider

Recursively images download from indicated site.

````
                                               ║
                                      ▄█▀▄     ║      ▄▀▄▄
                                     ▀    ▀▄   ║    ▄▀    ▀
                                     ▄▄▄    █▄▄▄▄▄▄█    ▄▄▄
                                   ▄▀   ▀█ █▀  ▐▌  ▀█ █▀   ▀▄
                                          ██  ▀▐▌▀  ██
                                     ▄█▀▀▀████████████▀▀▀▄▄
                                    █      ██████████      █
                                    █    █▀  ▀▀▀▀▀▀  ▀█    █
                                     ▀   █            █   ▀
                                           ▀        ▀
  
````

### Depth First Search algorithm
* * *

[Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search) algorithm to obtain links of all links extracted of main URL passed to program.


````py
DFS(G, u)
    u.visited = true
    for v in G.Adj[u]
        if v.visited == false
            DFS(G,v)

init()
    for u in G
        u.visited = false
     for u in G
       DFS(G, u)
````

#### Depth search scheme


````py
When I'm in node 'AAA', this pass to 'Visited' list, and then I found 'A', 
'M' and 'Q', that pass to 'Stack'.

                              ___ [AA] ____
Visited                      |      |      |
[AA][][][][]               _[A]   _[M]    [Q]
                          |      |    |
Stack                     [L]   [T]  [F]_
[A][M][Q][][]                            |
                                        [X]


Visited
[AA][A][][][]                 In the node 'A' (passed to visited) I found 'L',
Stack                         so I add it at front of stack
[L][M][Q][]


Visited
[AA][A][L][][]                In node 'L' (passed to visited) I didn't found anything
Stack                         so continue the stack to 'M'
[M][Q][][]


Visited                       In 'M', moved to 'visited', I found 'T' and 'F',
[AA][A][L][M][T][F]           pass it at front of stack.
Stack                         In 'T', nothing found, continue stack to 'F', where I found
[X][Q][][][]                  'X' and put it at front of stack.


Visited                     
[AA][A][L][M][T][F][X][Q]     In 'X', moved to 'visited', nothing found, and at final
Stack                         'Q' which is the last node.
[][][][][]                 

````
<br>

### ThreadPoolExecutor, run processes asyncronously
* * *

For each image url, executes download(). Using [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor) subclass, the execution speed increases significantly. This is an Executor subclass, an abstract class used to make asyncronously calls using specific number of threads, that are passed like an argument to class. 

<br>

>map()

Map() recieves two arguments, the task for apply to items (pass task without parameters) and the list of items to iterate and apply the task.
My download function only recieves one argument, the url to download. The another argument of map() is the list of urls that in other way I iterate in a for loop.

````py
with ThreadPoolExecutor(10) as executor:
	executor.map(download, urls)
````

[map()](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.map) unifies what would be a for loop in a single statement that returns an iterable object, which you can use later to analize items or check processes results.

<br>

>submit()

In my case I want to have more control over tasks while its being processed, not later. So for that, Executor have another function to run taks asyncronously, [submit()](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.submit), which executes task one by one, for each item.

<br>

````py
with ThreadPoolExecutor(10) as executor:
    for url in progbar(urls, 'Downloading '):
        executor.submit(download, url)
````

<br>

This method allows me to manage each task, for example, including a loading bar to see execution progress, or handle events like finished or running task or errors during Executor run.

<br><br>

#### **More info**
* * *

[ThreadPoolExecutor, map() vs submit()](https://superfastpython.com/threadpoolexecutor-map-vs-submit/)

[Thread carefully: an introduction to concurrent Python](https://hackaday.com/2018/12/18/thread-carefully-an-introduction-to-concurrent-python/)


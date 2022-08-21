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

Depth First Search algorithm to obtain links of all links extracted of main URL passed to program.

````python
DFS(G, u)
    u.visited = true
    for each v in G.Adj[u]
        if v.visited == false
            DFS(G,v)

init()
    for each u in G
        u.visited = false
     for each u in G
       DFS(G, u)
````

For each depth level, executes download() to obtain images. Using [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor) subclass, the execution speed increases significantly. This is a Executor subclass, an abstract class used to make asyncronously calls.

````python
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		executor.map(download, iterable)
````

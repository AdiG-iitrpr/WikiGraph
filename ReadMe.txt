Name:     Aditya Goel
Entry No: 2020MCB1259

You can find the full graph stored file here: "https://drive.google.com/file/d/1H0aEQcxps7GDEVJLX0byUdnAmCvP3I9d/view?usp=sharing"
The above file is used for the data results received.

There are 3 variables that define the files used in the program. To change any read or write factor, please consider changing them:
- dump_file: This variable stores the bz2 file name from where we extract the data
- graph_store_file: This variable stores the name of the file which stores all the title pages with links present in them in a text file.
- result_publish_file: This variable stores the name of file which will store the result of the random walk.

In the given project to create the wikigraph and run random walk, there are two main functions which span the entire code:

- dump_to_text(): In short, this function creates a text file containing titles of all pages with all the links stored in them.
                  - First we open the bz2 file and read it line by line.
                  - Then we check if "<page>" tag is present in the line which represents the starting of a webpage.
                  - We continue to read that page in a string format till we encounter "</page>" tag which represents end of webpage.
                  - Once done, we process this page before moving onto other one.
                  - Process of analysing the page is:
                    - Using Element Tree of xml parser of python, we figure out the title of page stored in variable name.
                    - Using regular expressions present in python, we try to read all the text present in "[[]]" representing
                      links in wikimarkup language.
                    - Regex returns names with square brackets contained which have to be removed.
                    - However, there are many unnecessary links like the ones containing "." or ":" or text in link after "|"
                      which have to be removed inorder for storing only the legit links.
                    - All this processing is done using string functions.
                  - Once done, we now have all the processed links in the variable links.
                  - Now we have to write the page data in the text file.
                    - We open the graph_store_file in append mode.
                    - First we write the title of page.
                    - It is followed by a "#" and then name of every link present in that page 
                    - In this way, we are able to store a single page in a single line.
                  - Once done, we have successfully read a page and we continue reading further pages till we reach end.

- text_to_graph_to_random_walk(): In short, this function converts the text stored in graph_store_file to adjacency list 
                                  and then performs a random walk on it and stores the result in result_publish_file.
                                  - We have to now read the graph from the text file and store in a dictionary.
                                  - The problem is we cannot store such a large file containing all names in a single variable.
                                  - It would destroy the RAM.
                                  - To optimise it, we assign an index to each title and link and store the adjacency list in form of indices.
                                  - We also make two maps of which mp1 stores index corresponding to title and mp2 which stores
                                    name corresponding to index.
                                  - Next, we perform random walk on the stored graph.
                                  - Once done, we store the results in result_publish_file.

- Observations:
    - We see that certain nodes always come on topmost visited whenever the random walk is run. Some of the top results include:
        - United States : 8345
        - The New York Times : 7736
        - World War II : 5381
        - France : 4431
        - List of sovereign states : 4238
        - United States Census Bureau : 4214
        - New York City : 3882
        - India : 3847
        - United Kingdom : 3665
        - Germany : 3639
    - The above results are for 10 million iterations of the random walk each one accompanying the frequency of visits.
    - By doing so, we visit approximately 4.5 million pages. (We can run random walk for 100 million but the result would
      come out approximately the same with an extra factor of 10. Also I was unable to run for such a large number due to
      some machine specific limitations.)
    - We observe that the pages on top are names of countries (which are obvious) and pages which may be linked to in many other pages.
    - This shows that the random walk on a data for many iterations provides us with pages having significantly more 
      inlinks and having a significant importance.
    - We also observe that pages such as World War is at top since many countries were invloved in it and had a large impact 
      on them.
    - Many famous newspaper names are also there.
    - I also found that 'Indian Institutes of Technology' was visited 30 times which was an exciting observation.
    - All this helps us in realising the importance of random walk for analysing big data.

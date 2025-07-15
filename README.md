# wikipedia_summariser
A tool for scrapping and summarising Wikipedia articles.

NOTES:
This project forced me to learn about a variety of different libraries, starting with bs4. I found understanding its functionality was actually quite simple, and was likely the least complex part of the process - other than the requests module, of course.

Requests was not originally involved. It was going to be selenium grabbing the url, but my dad introduced me to a far, far easier way of getting to a desired article. I assumed appending a Wikipedia URL with a topic name was going to be far more troublesome then it turned out.

The most difficult part was learning to use Hugging Face's transformers: that being said, I still have hardly a clue about LLMs. Before, the program utilised a spaCy cleaning stage for a better summary of the data. Trial showed spaCy to be a pointless addition to the overall project.

I found one of the trickier tasks in the end to be the error handling - it turns out it wasn't a difficult practice at all, but it surprised me I didn't even consider that things could still be inputted wrong. Plus, working out how a revised topic could still become the file name was surprisingly difficult. I had to use my first global variable. I'm glad I still find excitement in totally unexciting and meaningless things. It'll wear off.

Overall pleased with the project, but looking to understand JSON and HTML a little more off the back. A feature I wanted to include was the highlighting of unreferenced / unsupported information, but that'd take a little more understanding of HTML text scraping, or whatever. ANd JSON because it was a possible path to take, but I didn't. 

HTML, JSON, and more 'research tool' ideas. Perhaps experimenting with some popular, abundant libraries like pandas. Not completely sure.

Would like to move onto C# too - it might have to wait until I've produced a few more projects _on my own_.

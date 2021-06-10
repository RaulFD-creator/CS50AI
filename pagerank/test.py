import os
import random
import re
import sys

def main():
    damping_factor = 0.85
    n = 10000
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
   # corpus={"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "1.html"
    al = sample_pagerank(corpus, damping_factor, n)
    print(al)
   

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # If page has at least one outgoing link
    if corpus[page]:
        # Initialise probability distribution to P(page chosen at random out of all pages in corpus)
        total_probabilities = [(1 - damping_factor) / len(corpus)] * len(corpus)
        total_probabilities_dict = dict(zip(corpus.keys(), total_probabilities))

        # Add additional probability for all pages linked to by current page
        link_probabilities = damping_factor / len(corpus[page])
        for link in corpus[page]:
            total_probabilities_dict[link] += link_probabilities
        return total_probabilities_dict

    # If page has no outgoing links, probability distribution chooses randomly among all pages with equal probability
    else:
        return dict(zip(corpus.keys(), [1 / len(corpus)] * len(corpus)))

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise dictionary 
    keys = corpus.keys()
    sample = dict()
    
    for key in keys:
        sample[key] = 0
    
    # Random starting page
    random_page = random.choice(list(keys))

    for i in (range(n-1)):
        sample[random_page] += 1 / n
        prob = transition_model(corpus, random_page, damping_factor)
        random_page = random.choices(list(prob.keys()), prob.values())[0]
    
    return sample
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    page_rank = dict(zip(corpus.keys(), [1 / num_pages] * num_pages))
    page_rank_comp = dict(zip(corpus.keys(), [np.Inf] * num_pages))

    while any (page_rank_comp < 0.001 for page_rank_comp in page_rank_comp.values()):
        for page in page_rank.keys():
            link_prob = 0
            for link_page, links in corpus.items():
                if links is None:
                    links = corpus.keys()
                if page in links:
                    link_prob += page_rank[link_page] / len(links)
            new_page_rank = ((1-damping_factor) / num_pages) + (damping_factor * link_prob)
            page_rank_comp[page] = abs(new_page_rank - page_rank[page])
            page_rank[page] = new_page_rank
    return page_rank

main()

import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    
    # probability-list to initialize weights for random no. generator
    p = [damping_factor, 1 - damping_factor]
    prob = dict()
    linked = set()
    unlinked = set()
    
    # from the corpus, get the list of pages that the current page is linked to
    # and the list of pages the current page is not linked to
    # also set the transition model probabiilties to 0.0 initially
    for key, value in corpus.items():
        prob[key] = 0.0

        if key != page:
            continue
        else:
            linked = value
            unlinked = set()

        for key in corpus:
            if key in linked:
                continue
            else:
                unlinked.add(key)

    # each page starts with a base probability of reach of (1 - damping_factor)/total_pages
    # then each page linked to this page gets an additional probability of
    # damping_factor / no_of_links

    linked_count = len(linked)
    unlinked_count = len(unlinked)
    count = linked_count + unlinked_count
    prob_0 = p[1] / count

    for key in prob:
        
        if key in linked:
            prob[key] = prob_0+ damping_factor / linked_count
        else:
            prob[key] = prob_0

    return prob

        

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
    sample[random_page] += 1 / n

    for _ in (range(n-1)):
        prob = transition_model(corpus, random_page, damping_factor)
        next_pages = []
        probabilities = []
        for key, value in prob.items():
            next_pages.append(key)
            probabilities.append(value)

        random_page = random.choices(next_pages, weights=probabilities)[0]
        sample[random_page] += 1 / n

    return sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Total number of pages
    num_total_pages = len(corpus)

    # Start with 1/N for all pages
    rank_old = dict()
    for page in corpus:
        rank_old[page] = 1 / num_total_pages

    while True:
        rank_new = dict()

        # Calculate PageRank
        for page_new in corpus:
            rank_page_new = (1 - damping_factor) / num_total_pages
            for page, links in corpus.items():
                if links:
                    if page != page_new and page_new in links:
                        rank_page_new += damping_factor * (rank_old[page] / len(corpus[page]))

                else:
                    rank_page_new += damping_factor * (rank_old[page] / num_total_pages)
            rank_new[page_new] = rank_page_new

        # Stop if Ranks converged
        if rank_convergence(rank_new, rank_old):
            return rank_new

        rank_old = rank_new.copy()


def rank_convergence(new_rank, old_rank):
    for page in new_rank:

        # If new probability not calculated
        if not new_rank[page]:
            return False

        # Convergence at 0.001
        diff = new_rank[page] - old_rank[page]
        if diff > 0.001:
            return False
        
    return True

if __name__ == "__main__":
    main()
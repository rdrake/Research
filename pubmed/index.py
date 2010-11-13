from database import Indexer
from files import PubMedArticleExtractor
from progressbar import ProgressBar
from time import time

start_time = time()
pbar = ProgressBar().start()
extractor = PubMedArticleExtractor('/home/rdrake/datasets/pubmed')
extractor.cb_progress = lambda i: pbar.update(i / len(extractor) * 100)
extractor.cb_finished = lambda: pbar.finish()

indexer = Indexer('pubmed.idx')
indexer.index(extractor)

end_time = time()

print("Indexing took %f minutes." % ((end_time - start_time) / 60.0))

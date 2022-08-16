#!/usr/bin/env python

import helpers.IO as IO
from helpers.config import Config
from helpers.progress import Progress
from helpers.args import Args
from helpers.args import getConfigFile
from helpers.corpus import Corpus
from helpers.runner import Runner

if __name__ == "__main__":
    IO.printLine()
    print("Welcome to Algae!")
    IO.printLine()

    # import the config
    IO.printRaw('importing configuration... ')
    configFile = getConfigFile()
    config = Config(configFile)
    print("done!")

    # import the progress
    IO.printRaw('importing progress... ')
    progress = Progress(configFile)
    print("done!")

    # check program arguments, generate jobs
    IO.printRaw('checking arugments... ')
    args = Args(config)
    print("done!")

    # check the corpus
    IO.printRaw('checking corpus... ')
    corpus = Corpus(config)
    print("done!")
    IO.printLine()

    # run the jobs
    print("running jobs:\n")
    runner = Runner(config, progress, args, corpus)
    runner.run()

    # all done!
    IO.printLine()
    print("Goodbye!")
    IO.printLine()

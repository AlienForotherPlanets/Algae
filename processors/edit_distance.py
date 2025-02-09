# run an edit distance program (in C) pairwise on files
# assignment args:
# - entries (array):
# -- see preprocessors/mted.py
# - allowPartners (bool): Whether or not partners are allowed for this assignment.
# processor args:
# - sourceSuffix (string) - Suffix of file generated by preprocessor
# - resultsSuffix (string) - Suffix of file that will be written to postprocessor

import helpers.common as common
import helpers.IO as IO
import os
from multiprocessing import Process


def runEditDistance(path1, path2):
    handle = os.popen("./processors/bin/distance {} {}".format(path1, path2))
    distance = int(handle.read())
    handle.close()
    return distance

# THREAD CONTENT


def runEntry(entry, students, helpers, assignName, sourceSuffix, resultsSuffix, allowPartners):
    # create an empty PairResults object
    resultFilename = common.makeFilenameSafe(
        entry["sources"][0]) + resultsSuffix
    results = common.PairResults(assignName, resultFilename, helpers)

    # for each pair of students
    for i in range(len(students)):
        for j in range(i + 1):
            if i != j:
                # are these students partners?
                student1 = students[i]
                student2 = students[j]

                # get both file paths
                safeFilename = common.makeFilenameSafe(
                    entry["sources"][0]) + sourceSuffix
                path1 = helpers.getPreprocessedPath(
                    student1, assignName, safeFilename)
                path2 = helpers.getPreprocessedPath(
                    student2, assignName, safeFilename)

                # make sure both paths exist
                if path1 != None and path2 != None:
                    editDistance = runEditDistance(path1, path2)

                    # save the pair result
                    result = common.PairResult(
                        student1, student2, editDistance)
                    results.add(result)

    # flush results to disk
    results.finish()
    helpers.printf(
        "Finished '{}/{}'!\n".format(assignName, entry["sources"][0]))


def run(students, assignments, args, helpers):
    sourceSuffix = args["sourceSuffix"]
    resultsSuffix = args["resultsSuffix"]

    # threads to join later
    threads = []

    # for each assignment
    for assignment in assignments:
        # for each entry
        assignName = assignment.name
        allowPartners = assignment.args["allowPartners"]

        # print progress
        helpers.printf("processing '{}' in parellel...\n".format(assignName))

        entries = assignment.args["entries"]
        for entry in entries:
            # create the thread
            t = Process(target=runEntry, args=(entry, students, helpers,
                        assignName, sourceSuffix, resultsSuffix, allowPartners))
            threads.append(t)
            t.start()

    # join all of the threads
    for t in threads:
        t.join()

    # all done
    return True

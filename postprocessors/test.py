def run(students, assignments, args, helpers):
    helpers.printf("Postprocessor!\n")
    helpers.printf("{} students and {} assignments\n".format(
        len(students), len(assignments)))
    helpers.printf(args['message'] + '\n')
    return True

class FileHandler:

    @staticmethod
    def create_csv(file_path, logging_table):

        try:
            file = open(file_path, "a")
            for row in logging_table:
                for i, column in enumerate(row):
                    if i < 2:
                        file.write(f"{column}\t")
                    else:
                        file.write(f"{column}\n")
            file.close()
            return True

        except:
            return False

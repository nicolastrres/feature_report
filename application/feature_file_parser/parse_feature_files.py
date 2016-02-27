def get_feature(feature_file_path):
    feature_label = 'Feature:'
    with open(feature_file_path) as file:

        for line in file:
            if feature_label in line:
                return line[:-1]

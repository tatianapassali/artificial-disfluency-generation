from create_dataset import create_dataset

if __name__ == "__main__":


    create_dataset('/home/tatiana/PycharmProjects/artificial-disfluency-generation/data/sample_data/sample_data.csv',
                   '/home/tatiana/PycharmProjects/artificial-disfluency-generation/data/output_data',
                   column_text='text', percentages=[0,0,100],
                   concat_files=True,
                   create_all_files=True)

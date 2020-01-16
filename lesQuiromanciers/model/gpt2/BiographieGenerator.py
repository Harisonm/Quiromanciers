import gpt_2_simple as gpt2
import flask
import os
import requests


class BiographieGenerator:
    def __init__(self, model_name: str,run_name: str):
        self.model_name = model_name
        self.run_name = run_name

    def prepare_fine_tuning(self,file_name : str):
        if not os.path.isdir(os.path.join("models", self.model_name)):
            print(f"Downloading {self.model_name} model...")
            gpt2.download_gpt2(
                model_name=self.model_name
            )  # model is saved into current directory under /models/124M/

        sess = gpt2.start_tf_sess()

        gpt2.finetune(
            sess,
            dataset=file_name,
            model_name=self.model_name,
            steps=1000,
            restore_from="fresh",
            run_name="run1",
            print_every=10,
            sample_every=200,
            save_every=500,
        )
        # sess = gpt2.start_tf_sess()

        # gpt2.load_gpt2(sess, run_name='run1')
        # gpt2.generate(sess, run_name='run1')

    def load_a_trained_model_checkpoint():
        pass

    # def generate_to_file(self):
    #     gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())

    #     gpt2.generate_to_file(sess,
    #                         destination_path=gen_file,
    #                         length=500,
    #                         temperature=0.7,
    #                         nsamples=100,
    #                         batch_size=20
    #                         )
    #     # may have to run twice to get file to download
    #     files.download(gen_file)

    def generate_biographie(self, prefix: str):
        
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name=self.run_name)
        
        return gpt2.generate(
            sess,
            length=250,
            temperature=0.7,
            prefix=prefix,
            return_as_list=True,
            nsamples=5,
            batch_size=5,
        )

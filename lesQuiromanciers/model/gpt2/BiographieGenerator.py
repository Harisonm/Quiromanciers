import gpt_2_simple as gpt2
import os
import requests


class BiographieGenerator:
    """
     Classe Qui construit un modèle depuis le modèle GPT2 de OpenIA.
    """
    def __init__(self, model_name: str,run_name: str):
        """
        __init__ : Initialise la classe BiographieGenerator avec des arguments.
        
        Args:
            model_name (str): Nom du model.
            run_name (str): Nom du run_name du modèle GPT2 utilisé lors de l'apprentissage.
        """
        self.model_name = model_name
        self.run_name = run_name

    def prepare_fine_tuning(self,file_name : str):
        """
        prepare_fine_tuning : Personnalise et regle le modèle pour l'entrainer sur notre dataset.
        
        Args:
            file_name (str): Nom du fichier d'entrée.
        """
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
            run_name=self.run_name,
            print_every=10,
            sample_every=200,
            save_every=500,
        )

    def generate_biographie(self, prefix: str):
        """
        generate_biographie: 
        
        Args:
            prefix (str): Premier partie de la biographie donnée pour le modele afin qu'il continu les prochaines phrases automatiquement.
        
        Returns:
            list: Biographie dans une liste.
        """
        
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

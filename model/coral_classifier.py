import bentoml
from bentoml.frameworks.fastai import FastaiModelArtifact
from bentoml.adapters import FileInput
from fastcore.utils import tuplify, detuplify


with open('requirements.txt') as f:
    packages = [p.strip() for p in f.readlines()]


@bentoml.env(pip_packages=packages)
@bentoml.artifacts([FastaiModelArtifact('learner')])
class CoralClassifier(bentoml.BentoService):

    @bentoml.api(input=FileInput(), batch=False)
    def predict(self, files):
        files = [i.read() for i in files]

        dl = self.artifacts.learner.dls.test_dl(files, rm_type_tfms=None, num_workers=0)
        inp, preds, _, dec_preds = self.artifacts.learner.get_preds(dl=dl, with_input=True, with_decoded=True)
        i = getattr(self.artifacts.learner.dls, 'n_inp', -1)
        inp = (inp,)
        dec_list = self.artifacts.learner.dls.decode_batch(inp + tuplify(dec_preds))
        res = []
        for dec in dec_list:
            dec_inp, dec_targ = map(detuplify, [dec[:i], dec[i:]])
            res.append(dec_targ)

        return res
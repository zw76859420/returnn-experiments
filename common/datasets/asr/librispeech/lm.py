
from ....models.lstm import make_lstm, make_net
from ....models.lm import Lm
from .vocabs import bpe1k


class Lstm4x2048AndreBpe1k(Lm):
  vocab = bpe1k

  opts = dict(
    embed_dim=128, embed_with_bias=True,
    num_layers=4, lstm_dim=2048,
  )

  net_dict = {
    "lstm": make_lstm(**opts),
    "output": {
      "class": "linear", "activation": "log_softmax", "use_transposed_weights": True,
      "n_out": vocab.get_num_classes(), "from": "lstm"}
  }

  # 15.4 PPL, from ITC, 20 + 7 (pretrained)
  # _lm_model = "/work/asr3/zeyer/merboldt/librispeech/2020-09-04--librispeech-rnnt-rna/data-train/lm_lstm_baseline_4_2048.bpe1k/net-model-retrained-on-mgpu-itc/network.020"
  model_path = "data-common/librispeech/lm/andre_lstm_bpe1k_lm/net-model/network.020"

#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy
import os


my_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.normpath(my_dir + "/../figures/ctc2020")


def plot_alignment(alignment, labels, filename=None):
  """
  :param list[int]|list[list[float]] alignment:
  :param list[str] labels:
  :param str|None filename:
  """
  num_labels = len(labels)
  num_frames = len(alignment)
  ts = range(num_frames)

  if isinstance(alignment[0], list):
    assert len(alignment[0]) == num_labels
    ss = numpy.array(alignment).transpose()
    assert ss.shape == (num_labels, num_frames)
  else:
    assert max(alignment) == num_labels
    ss = [[0.0] * num_frames for _ in range(num_labels)]
    for t, a in enumerate(alignment):
      ss[a - 1][t] = 1.

  fig = plt.figure(frameon=False, figsize=(5, 0.8))
  extra_height = 0.2  # 0.07
  ax = fig.add_axes([0, extra_height, 1, 1. - 2 * extra_height])
  ax.axis('off')

  # fig, ax = plt.subplots(
  #   subplot_kw=dict(aspect=22),
  #   figsize=(6, 2),
  #   tight_layout=True,
  #   frameon=False)

  assert isinstance(fig, plt.Figure)
  # fig.patch.set_visible(False)
  assert isinstance(ax, plt.Axes)
  # ax.set_aspect(20)

  # ax.set_axis_off()
  # ax.tick_params(axis='both')
  # ax.set(xlabel='t', ylabel='p_t(s|x)', title='Alignment')
  # ax.grid()

  for i, s in enumerate(ss):
    kwargs = {}
    if i == len(ss) - 1:  # last label
      kwargs.update(dict(color='lightgray', linestyle='dotted'))
    ax.plot(ts, s, **kwargs)
    if i < len(ss) - 1:
      xmax = numpy.argmax(s)
      ymax = s[xmax]
      xmax2 = xmax
      while s[xmax2] == ymax:
        xmax2 += 1
      xmax = (xmax2 - 1 + xmax) / 2.
      ax.annotate(labels[i], xy=(xmax, ymax), ha="center", fontsize=16)

  if filename:
    filename = "%s/%s" % (target_dir, filename)
    print("save figure:", filename)
    fig.savefig(filename)
  else:
    plt.show()


def main():
  labels = ["p", "ih", "ng", "sil"]
  labels_blank = labels[:-1] + ["blank"]

  # example for ex:ping:
  # $s_1^T = (4^{40}, 1, 2, 3, 4^{40})$
  n_ = 10
  align_opt_sil = [4] * 2 * n_ + [1] * n_ + [2] * 3 * n_ + [3] * 2 * n_ + [4] * 2 * n_
  # Trained FFNN with bias via simple_model.py, resulting Viterbi alignment.
  align_peaky_sil = [x + 1 for x in [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
  align_peaky_blank = [x + 1 for x in [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
  assert len(align_peaky_sil) == len(align_peaky_blank) == len(align_opt_sil)

  posteriors_blank = (
    [[1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [0.11329136788845062, 7.64282859222476e-08, 5.0091447434397196e-08, 0.8867084980010986],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [4.815770449084766e-09, 0.03436011075973511, 1.1281462874990211e-08, 0.9656398296356201],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [8.512160754037268e-09, 1.6339818387223204e-08, 0.051136527210474014, 0.9488635063171387],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0],
     [1.2303150165315913e-10, 4.677016551823954e-10, 2.2791392384480247e-10, 1.0]])
  posteriors_sil = (
    [[5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [5.60422863671306e-09, 6.19781515606016e-13, 2.275723880174052e-11, 1.0],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [0.034249208867549896, 0.03456207364797592, 0.03506220132112503, 0.8961265087127686],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [4.967092709362575e-11, 3.9665035700409135e-09, 6.305710121523589e-05, 0.9999369382858276],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0],
     [5.429683178764799e-12, 1.506674125739682e-11, 8.984882282625506e-11, 1.0]])

  plot_alignment(alignment=align_opt_sil, labels=labels, filename="ex-ping-opt-sil.pdf")
  plot_alignment(alignment=align_peaky_sil, labels=labels, filename="ex-ping-peaky-sil.pdf")
  plot_alignment(alignment=align_peaky_blank, labels=labels_blank, filename="ex-ping-peaky-blank.pdf")

  plot_alignment(alignment=posteriors_sil, labels=labels, filename="ex-ping-posteriors-sil.pdf")
  plot_alignment(alignment=posteriors_blank, labels=labels, filename="ex-ping-posteriors-blank.pdf")


if __name__ == '__main__':
  import better_exchook
  better_exchook.install()
  main()

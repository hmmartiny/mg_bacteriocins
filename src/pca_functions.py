import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import TransformedBbox
import seaborn as sns

def _arrow_annotate(axis, x, y, label):
    ann = axis.annotate(
        str(label)[:30],
        (x, y),
        ha='left',
        va='bottom',
        alpha = .75,
        color='black',
        zorder=5001
    )
    
    fig = axis.get_figure()
    fig.canvas.draw()
    bbox = ann.get_window_extent(renderer=fig.canvas.get_renderer())
    transform = axis.transData.inverted() 
    tbox = TransformedBbox(bbox, transform).corners()

    if tbox[2][0] > axis.get_xlim()[1]:
        axis.texts[-1]._x -= (tbox[2][0]-axis.get_xlim()[1])
        fig.canvas.draw()
        bbox = axis.texts[-1].get_window_extent(renderer=fig.canvas.get_renderer())
        transform = axis.transData.inverted()
        tbox = TransformedBbox(bbox, transform).corners()
        axis.texts[-1]._x += (axis.get_xlim()[1]-tbox[2][0])

def adjustloadinglabels(axis):
    ''' Adjust loading label positions, so that labels don't overlap. '''
    fig = axis.get_figure()
    fig.canvas.draw()
    for idx, label in enumerate(axis.texts[:-1]):
        bbox = label.get_window_extent(renderer=fig.canvas.get_renderer())
        transform = axis.transData.inverted()
        tbox = TransformedBbox(bbox, transform).corners()
        for tidx, testlabel in enumerate(axis.texts[idx+1:]):
            lbox = testlabel.get_window_extent(
                renderer=fig.canvas.get_renderer())
            transform = axis.transData.inverted()
            ttbox = TransformedBbox(lbox, transform).corners()
            if _do_bbox_overlap(tbox, ttbox) or _do_bbox_overlap(ttbox, tbox):
                if axis.texts[idx]._y < axis.texts[idx+tidx+1]._y:
                    axis.texts[idx]._y -= (tbox[1][1]-tbox[0][1])/3.
                    axis.texts[idx+tidx+1]._y += (ttbox[1][1]-ttbox[0][1])/3.
                else:
                    axis.texts[idx]._y += (tbox[1][1]-tbox[0][1])/3.
                    axis.texts[idx+tidx+1]._y -= (ttbox[1][1]-ttbox[0][1])/3.
                fig.canvas.draw()

def _do_bbox_overlap(box1, box2):
    # If one rectangle is on left side of other
    if box1[1][0] > box2[2][0] or box2[1][0] > box1[2][0]:
        return False

    # If one rectangle is above other
    if box1[3][1] > box2[1][1] or box2[2][1] > box1[1][1]:
        return False

    return True

def _plot_loadings(axis, loadings, scale=None, cutoff=0):
    
    if scale is None:
        scale = np.max(np.abs(loadings.values))
    
    labels = loadings.columns
    
    x, y = loadings.index.tolist()
    
    loadings.loc['len'] = [
        np.sqrt(
            pow(loadings.loc[x, column], 2) + 
            pow(loadings.loc[y, column], 2))
        for column in loadings.columns
    ]
        
    
    if cutoff > 0:
        loadings = loadings.T.query(f"len > {cutoff}").T
    
    for column in loadings:
        axis.arrow(
            0, 0,
            loadings.loc[x, column],
            loadings.loc[y, column],
            facecolor='black',
            alpha = .5,
            linewidth = 0,
            width = scale * 0.01,
            zorder=2000
        )
        
        if loadings.loc['len', column] > cutoff:
            _arrow_annotate(axis, loadings.loc[x, column], loadings.loc[y, column], column)

def plot_scores(axis, scores, palette, colorgroup, kind='scatter', zorder=7, **kwargs):
    
    if kind == 'scatter':
        sns.scatterplot(
            data = scores,
            x = scores.columns[0],
            y = scores.columns[1],
            hue=colorgroup,
            palette=palette,
            ax=axis,
            alpha = kwargs.get('scatter_alpha', .5),
            zorder=zorder,
            legend=kwargs.get('legend', True)
        )
    elif kind == 'contour':
        sns.kdeplot(
            data = scores,
            x = scores.columns[0],
            y = scores.columns[1],
            hue=colorgroup,
            palette=palette,
            ax=axis,
            alpha = kwargs.get('contour_alpha', .5),
            zorder=zorder,
            warn_singular=False,
            fill=True,
            levels=kwargs.get('contour_levels', 10),
            thresh=kwargs.get('contour_thresh', 0.05),
            legend=kwargs.get('legend', True)
        )
        
def pca_biplot(scores, loadings, meta, scales=None, x='pc1', y='pc2', eig_val=None, axis=None, figsize=(7,7), **kwargs):
    
    if scales is None:
        scales = [
            np.max(np.abs(loadings.values)),
            [np.max(np.abs(scores.loc[idx].values)) for idx in [[x, y]]]
        ]
    
    if axis is None:
        _, axis = plt.subplots(figsize=figsize)
    
    # set xlabel and ylabel
    if eig_val is not None:
        axis.set_xlabel(f"{x.upper()} ({eig_val.loc[x, 'expvar']:.1f}% explained variation)")
        axis.set_ylabel(f"{y.upper()} ({eig_val.loc[y, 'expvar']:.1f}% explained variation)")
    
    # set axes limits
    axis.set_xlim(-scales[0]*1.1, scales[0]*1.1)
    axis.set_ylim(-scales[0]*1.1, scales[0]*1.1)
    
    # prettify
    axis.axhline(color='black', alpha=.4, ls='--')
    axis.axvline(color='black', alpha=.4, ls='--')
    
    
    # plot loadings
    _plot_loadings(axis=axis, loadings=loadings.loc[[x,y]], scale=scales[0], cutoff=kwargs.get('cutoff', 1))
    adjustloadinglabels(axis)
    
    # plot scores
    scores_meta = scores.loc[[x, y]].T.merge(meta, left_index=True, right_on=kwargs.get('sample_key', 'run_accession'))
    scores_meta.set_index(kwargs.get('sample_key', 'run_accession'), inplace=True)

    kinds = kwargs.pop('kinds', ['scatter'])
    for i, kind in enumerate(kinds):
        plot_scores(axis, scores_meta, kind=kind, zorder=7+i, legend=i==0, **kwargs)

    return axis
